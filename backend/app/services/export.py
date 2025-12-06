from io import BytesIO
from typing import Iterable

from openpyxl import Workbook

from ..models.invoice import Invoice


def build_invoice_workbook(invoices: Iterable[Invoice]) -> BytesIO:
    invoice_list = list(invoices)

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Facturas"

    headers = [
        "ID",
        "Tipo operación",
        "Tipo documento",
        "NCF",
        "RNC emisor",
        "Fecha comprobante",
        "Monto facturado",
        "ITBIS",
        "Pago efectivo",
        "Pago tarjeta",
        "Venta crédito",
        "Origen",
        "Validación",
        "Ruta archivo",
    ]
    sheet.append(headers)

    for invoice in invoice_list:
        totals = invoice.totals or {}
        payments = invoice.payments or {}
        sheet.append(
            [
                invoice.id,
                invoice.tipo_operacion,
                invoice.tipo_documento,
                invoice.ncf,
                invoice.rnc_emisor,
                invoice.fecha_comprobante.isoformat(),
                getattr(totals, "monto_facturado", None),
                getattr(totals, "itbis_facturado", None),
                getattr(payments, "monto_efectivo", None),
                getattr(payments, "monto_tarjeta", None),
                getattr(payments, "monto_venta_credito", None),
                invoice.origen,
                invoice.validation_status,
                invoice.file_url,
            ]
        )

    summary_sheet = workbook.create_sheet("Resumen")
    summary_sheet.append(["Total facturas", len(invoice_list)])
    summary_sheet.append(["Nota", "Export generado desde FastAPI"])

    stream = BytesIO()
    workbook.save(stream)
    stream.seek(0)
    return stream
