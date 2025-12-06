from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from ..database import get_session
from ..models.invoice import Invoice, InvoiceTotals, PaymentBreakdown
from ..schemas import InvoiceCreate, InvoiceRead
from ..telegram import send_invoice_notification

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


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(
    payload: InvoiceCreate, session: Session = Depends(get_session)
) -> Invoice:
    invoice_data = payload.dict(exclude={"totals", "pagos"})
    invoice = Invoice(**invoice_data)
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
