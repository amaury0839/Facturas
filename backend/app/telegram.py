from os import getenv
from typing import Optional

import httpx

from .models.invoice import Invoice


def _build_message(invoice: Invoice) -> str:
    receptor = invoice.nombre_receptor or invoice.rnc_receptor or "N/D"
    emisor = invoice.nombre_emisor or invoice.rnc_emisor
    totals = invoice.totals

    monto = None
    if totals:
        monto = totals.monto_facturado or totals.monto_facturado_bienes or totals.monto_facturado_servicios

    lines = [
        "Nueva factura registrada",
        f"ID interno: {invoice.id}",
        f"Origen: {invoice.origen.value}",
        f"Tipo: {invoice.tipo_operacion.value} / {invoice.tipo_documento.value}",
        f"Emisor: {emisor}",
        f"Receptor: {receptor}",
        f"NCF: {invoice.ncf}",
        f"Fecha: {invoice.fecha_comprobante.isoformat()}",
    ]

    if monto is not None:
        lines.append(f"Monto facturado: {monto}")

    if invoice.comentarios:
        lines.append(f"Notas: {invoice.comentarios}")

    return "\n".join(lines)


def send_invoice_notification(invoice: Invoice) -> Optional[httpx.Response]:
    bot_token = getenv("TELEGRAM_BOT_TOKEN")
    chat_id = getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        return None

    message = _build_message(invoice)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    try:
        response = httpx.post(url, json={"chat_id": chat_id, "text": message})
        response.raise_for_status()
        return response
    except httpx.HTTPError:
        return None
