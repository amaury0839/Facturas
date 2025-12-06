from __future__ import annotations

from datetime import datetime
from pathlib import Path
import tempfile
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from ..config import Settings, get_settings
from ..schemas_telegram import TelegramMessage, TelegramUpdate, TelegramWebhookResponse
from ..services.google_archiver import InvoiceArchiver
from ..services.telegram import TelegramBotClient

router = APIRouter(prefix="/telegram", tags=["telegram"])

COMPANY_BY_CHAT: dict[int, str] = {}
DEFAULT_COMPANY = "Generico"
_archiver: Optional[InvoiceArchiver] = None


def _validate_token(query_token: str | None, settings: Settings) -> None:
    if settings.telegram_webhook_secret and query_token != settings.telegram_webhook_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook token")


def _get_archiver(settings: Settings) -> InvoiceArchiver:
    global _archiver

    if not settings.drive_folder_id:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Drive folder not configured")

    service_account_path = Path(settings.google_service_account_file)
    if not service_account_path.exists():
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service account file not found")

    if _archiver is None:
        _archiver = InvoiceArchiver(
            drive_folder_id=settings.drive_folder_id,
            service_account_file=str(service_account_path),
            sheet_id=settings.sheet_id,
        )

    return _archiver


async def _download_telegram_file(bot_token: str, file_id: str, filename: str) -> Path:
    base_url = f"https://api.telegram.org/bot{bot_token}"
    async with httpx.AsyncClient() as client:
        file_info_response = await client.get(f"{base_url}/getFile", params={"file_id": file_id})
        file_info_response.raise_for_status()
        file_path = file_info_response.json().get("result", {}).get("file_path")
        if not file_path:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not retrieve file path from Telegram")

        download_response = await client.get(f"https://api.telegram.org/file/bot{bot_token}/{file_path}")
        download_response.raise_for_status()

    suffix = Path(filename).suffix or Path(file_path).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(download_response.content)
        return Path(temp_file.name)


def _parse_company_command(text: str) -> Optional[str]:
    content = text.replace("/empresa", "", 1).strip()
    return content or None


async def _handle_invoice_upload(message: TelegramMessage, settings: Settings, empresa: str) -> str:
    if not message.document and not message.photo:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No attachment found")

    filename: str
    file_id: str

    if message.document:
        filename = message.document.file_name or "factura.pdf"
        file_id = message.document.file_id
    else:
        photo = message.photo[-1]
        filename = f"factura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        file_id = photo.file_id

    local_path = await _download_telegram_file(settings.telegram_bot_token, file_id, filename)
    now = datetime.now()
    archiver = _get_archiver(settings)

    try:
        drive_file_id = archiver.upload_to_drive_by_month(local_path, filename, now)
        archiver.append_invoice_to_sheet(now, empresa, drive_file_id)
    finally:
        if local_path.exists():
            local_path.unlink()

    return (
        "✅ Factura guardada.\n"
        f"Mes: *{now.strftime('%Y-%m')}*\n"
        f"Empresa: *{empresa}*\n"
        f"Archivo: `{filename}`\n"
        f"Fecha: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        "Organizada por mes en tu Google Drive y registrada en tu Google Sheet."
    )


async def _handle_text_commands(bot: TelegramBotClient, chat_id: int, message: TelegramMessage) -> bool:
    if not message.text:
        return False

    if message.text.startswith("/start"):
        await bot.send_message(
            chat_id=chat_id,
            text=(
                "Hola 👋\n"
                "Soy tu bot de facturas.\n\n"
                "1️⃣ Usa /empresa Nombre_Empresa para seleccionar la empresa.\n"
                "2️⃣ Envíame una foto o PDF de la factura.\n\n"
                "Yo la guardaré en Google Drive organizada por *mes* (YYYY-MM) "
                "y la registraré en tu Google Sheet con la empresa que selecciones. 💼📂"
            ),
        )
        return True

    if message.text.startswith("/empresa"):
        empresa = _parse_company_command(message.text)
        if not empresa:
            await bot.send_message(
                chat_id=chat_id,
                text=("Por favor indica el nombre de la empresa. Ejemplo:\n/empresa Colmado Pepe"),
                reply_to_message_id=message.message_id,
            )
            return True

        COMPANY_BY_CHAT[chat_id] = empresa
        await bot.send_message(
            chat_id=chat_id,
            text=(
                "Perfecto, a partir de ahora las facturas se registrarán para la empresa:\n"
                f"*{empresa}*"
            ),
            reply_to_message_id=message.message_id,
        )
        return True

    return False


@router.post("/webhook", response_model=TelegramWebhookResponse)
async def handle_webhook(
    update: TelegramUpdate, token: str | None = None, settings: Settings = Depends(get_settings)
) -> TelegramWebhookResponse:
    if not settings.telegram_bot_token:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Telegram bot token not configured")

    _validate_token(token, settings)

    chat_id = update.effective_chat_id
    if not chat_id or not update.message:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No chat information in update")

    bot = TelegramBotClient(settings.telegram_bot_token)

    handled_text = await _handle_text_commands(bot, chat_id, update.message)
    if handled_text:
        return TelegramWebhookResponse(ok=True, message="Command processed")

    if update.message.document or update.message.photo:
        empresa = COMPANY_BY_CHAT.get(chat_id, DEFAULT_COMPANY)
        confirmation_text = await _handle_invoice_upload(update.message, settings, empresa)
        await bot.send_message(chat_id=chat_id, text=confirmation_text, reply_to_message_id=update.message.message_id)
        return TelegramWebhookResponse(ok=True, message="Invoice saved")

    await bot.send_message(
        chat_id=chat_id,
        text=(
            "Recibimos tu mensaje para Facturas 606/607.\n"
            f"Texto: {update.summary_text}\n\n"
            "Envía tus facturas en PDF o imagen para iniciar el proceso."
        ),
        reply_to_message_id=update.message.message_id,
    )

    return TelegramWebhookResponse(ok=True, message="Webhook processed")
