# Backend FastAPI inicial

Base mínima para el servicio FastAPI que gestionará las facturas 606/607 descritas en `docs/architecture.md`.

## Requisitos
- Python 3.11+
- Dependencias de `requirements.txt`

Variables de entorno útiles:
- `FACTURAS_TELEGRAM_BOT_TOKEN`: Token de bot de Telegram utilizado para enviar respuestas.
- `FACTURAS_TELEGRAM_WEBHOOK_SECRET`: Token opcional para validar el query param `token` en `/telegram/webhook`.

## Uso rápido
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Variables de entorno opcionales:
- `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` para enviar notificaciones cuando se crea una factura.

La base de datos SQLite `data.db` se crea al iniciar la app y define tablas básicas para facturas, totales y desglose de pagos.
Endpoints iniciales:
- `GET /health`
- `POST /invoices`
- `GET /invoices`
- `GET /invoices/{id}`

Consulta `../docs/deployment.md` para un manual de despliegue detallado.
- `POST /telegram/webhook?token=...`
