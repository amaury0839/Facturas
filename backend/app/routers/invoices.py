from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models.invoice import Invoice, InvoiceTotals, PaymentBreakdown
from ..schemas import InvoiceCreate, InvoiceRead

router = APIRouter(prefix="/invoices", tags=["invoices"])


def _save_totals(session: Session, invoice_id: int, data: InvoiceCreate) -> None:
    if data.totals:
        totals = InvoiceTotals(
            invoice_id=invoice_id, **data.totals.model_dump(exclude_none=True)
        )
        session.add(totals)


def _save_payments(session: Session, invoice_id: int, data: InvoiceCreate) -> None:
    if data.pagos:
        payments = PaymentBreakdown(
            invoice_id=invoice_id, **data.pagos.model_dump(exclude_none=True)
        )
        session.add(payments)


@router.post("", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(
    payload: InvoiceCreate, session: Session = Depends(get_session)
) -> Invoice:
    invoice_data = payload.model_dump(exclude={"totals", "pagos"}, exclude_none=True)
    invoice = Invoice(**invoice_data)
    session.add(invoice)
    session.commit()
    session.refresh(invoice)

    _save_totals(session, invoice.id, payload)
    _save_payments(session, invoice.id, payload)
    session.commit()

    return invoice


@router.get("", response_model=list[InvoiceRead])
def list_invoices(session: Session = Depends(get_session)) -> list[Invoice]:
    statement = select(Invoice)
    return session.exec(statement).all()


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, session: Session = Depends(get_session)) -> Invoice:
    invoice = session.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found")
    return invoice
