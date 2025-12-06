from typing import Any

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, func, select

from .database import get_session, init_db
from .models.invoice import Invoice
from .paths import UPLOADS_DIR
from .routers import invoices, telegram

app = FastAPI(title="Facturas DGII 606/607")

app.include_router(invoices.router)
app.include_router(telegram.router)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health", tags=["health"])
def healthcheck(session: Session = Depends(get_session)) -> dict[str, Any]:
    try:
        total_invoices = session.exec(select(func.count()).select_from(Invoice)).one()
    except Exception:
        return {"status": "error", "message": "DB check failed"}

    return {"status": "ok", "invoice_count": total_invoices}
