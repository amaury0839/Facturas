from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from .. import schemas

from ..database import get_session
from ..models.invoice import Invoice, InvoiceTotals, PaymentBreakdown
from ..schemas import InvoiceCreate, InvoiceRead
from ..paths import UPLOADS_DIR
from ..telegram import send_invoice_notification
from ..services.export import build_invoice_workbook

router = APIRouter(prefix="/invoices", tags=["invoices"])


def _save_totals(
    session: Session, invoice_id: int, data: InvoiceCreate
) -> Optional[InvoiceTotals]:
    if data.totals:
        totals = InvoiceTotals(invoice_id=invoice_id, **data.totals.dict())
        session.add(totals)
        return totals

    return None


def _save_payments(
    session: Session, invoice_id: int, data: InvoiceCreate
) -> Optional[PaymentBreakdown]:
    if data.pagos:
        payments = PaymentBreakdown(invoice_id=invoice_id, **data.pagos.dict())
        session.add(payments)
        return payments

    return None


def _persist_invoice(session: Session, payload: InvoiceCreate) -> Invoice:
    invoice_data = payload.dict(exclude={"totals", "pagos"})
    invoice = Invoice(**invoice_data)
    invoice.updated_at = datetime.utcnow()
    session.add(invoice)
    session.commit()
    session.refresh(invoice)

    totals = _save_totals(session, invoice.id, payload)
    payments = _save_payments(session, invoice.id, payload)
    session.commit()
    session.refresh(invoice)

    if totals:
        session.refresh(totals)
        invoice.totals = totals
    if payments:
        session.refresh(payments)
        invoice.payments = payments

    send_invoice_notification(invoice)

    return invoice


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(
    payload: InvoiceCreate, session: Session = Depends(get_session)
) -> Invoice:
    return _persist_invoice(session, payload)


@router.get("", response_model=list[InvoiceRead])
def list_invoices(session: Session = Depends(get_session)) -> list[Invoice]:
    statement = select(Invoice).options(
        selectinload(Invoice.totals), selectinload(Invoice.payments)
    )
    return session.exec(statement).all()


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, session: Session = Depends(get_session)) -> Invoice:
    statement = (
        select(Invoice)
        .where(Invoice.id == invoice_id)
        .options(selectinload(Invoice.totals), selectinload(Invoice.payments))
    )
    invoice = session.exec(statement).one_or_none()
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice


@router.post("/upload", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
async def upload_invoice(
    metadata: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> Invoice:
    try:
        payload = InvoiceCreate.parse_raw(metadata)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Metadata inválida: {exc}"
        ) from exc

    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{uuid4().hex}_{file.filename}"
    saved_path = UPLOADS_DIR / safe_name
    content = await file.read()
    saved_path.write_bytes(content)

    payload.file_url = f"/uploads/{safe_name}"
    payload.file_mime = file.content_type
    payload.file_size = len(content)
    payload.origen = payload.origen or schemas.OrigenFactura.WEB

    invoice = _persist_invoice(session, payload)
    invoice.file_url = payload.file_url
    invoice.file_mime = payload.file_mime
    invoice.file_size = payload.file_size
    invoice.updated_at = datetime.utcnow()
    session.add(invoice)
    session.commit()
    session.refresh(invoice)
    return invoice


@router.get("/export", response_class=StreamingResponse)
def export_invoices(
    tipo_operacion: Optional[schemas.TipoOperacion] = None,
    session: Session = Depends(get_session),
) -> StreamingResponse:
    statement = select(Invoice).options(
        selectinload(Invoice.totals), selectinload(Invoice.payments)
    )
    if tipo_operacion:
        statement = statement.where(Invoice.tipo_operacion == tipo_operacion)

    invoices = session.exec(statement).all()
    workbook_stream = build_invoice_workbook(invoices)

    timestamp = datetime.utcnow().strftime("%Y%m%d")
    tipo_label = tipo_operacion.value if tipo_operacion else "606-607"
    headers = {
        "Content-Disposition": f"attachment; filename=facturas_{tipo_label}_{timestamp}.xlsx"
    }
    return StreamingResponse(
        workbook_stream,
        media_type=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
        headers=headers,
    )
