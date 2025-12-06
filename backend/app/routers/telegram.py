from fastapi import APIRouter, Depends, HTTPException, status

from ..config import Settings, get_settings
from ..schemas_telegram import TelegramUpdate, TelegramWebhookResponse
from ..services.telegram import TelegramBotClient

router = APIRouter(prefix="/telegram", tags=["telegram"])


def _validate_token(query_token: str | None, settings: Settings) -> None:
    if settings.telegram_webhook_secret and query_token != settings.telegram_webhook_secret:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid webhook token")


@router.post("/webhook", response_model=TelegramWebhookResponse)
async def handle_webhook(
    update: TelegramUpdate, token: str | None = None, settings: Settings = Depends(get_settings)
) -> TelegramWebhookResponse:
    if not settings.telegram_bot_token:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Telegram bot token not configured")

    _validate_token(token, settings)

    chat_id = update.effective_chat_id
    if not chat_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No chat information in update")

    bot = TelegramBotClient(settings.telegram_bot_token)
    reply_text = (
        "Recibimos tu mensaje para Facturas 606/607.\n"
        "Texto: "
        f"{update.summary_text}\n\n"
        "Envía tus facturas en PDF o imagen para iniciar el proceso."
    )

    await bot.send_message(chat_id=chat_id, text=reply_text, reply_to_message_id=update.message.message_id if update.message else None)

    return TelegramWebhookResponse(ok=True, message="Webhook processed")
