# Backend FastAPI inicial

Base mínima para el servicio FastAPI que gestionará las facturas 606/607 descritas en `docs/architecture.md`.

## Requisitos
- Python 3.11+
- Dependencias de `requirements.txt`

## Uso rápido
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

La base de datos SQLite `data.db` se crea al iniciar la app y define tablas básicas para facturas, totales y desglose de pagos. Endpoints iniciales:
- `GET /health`
- `POST /invoices`
- `GET /invoices`
- `GET /invoices/{id}`
