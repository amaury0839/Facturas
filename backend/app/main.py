from fastapi import FastAPI

from .database import init_db
from .routers import invoices

app = FastAPI(title="Facturas DGII 606/607")

app.include_router(invoices.router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
