# Facturas

Diseño y lineamientos para una aplicación que gestiona facturas de compras (606) y ventas (607) para DGII en República Dominicana.

Consulta `docs/architecture.md` para la arquitectura, modelo de datos, flujos, validaciones y pseudocódigo clave.

## Puesta en marcha rápida

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # instala uvicorn y demás dependencias
uvicorn app.main:app --reload    # ejecuta desde el directorio backend
```

Si se ejecuta `uvicorn` desde la raíz del repositorio sin instalar las dependencias en `backend/`, el comando no estará disponible en el entorno virtual.

## Backend
- Backend inicial en FastAPI en `backend/` con modelos SQLModel para facturas, totales y pagos.
- Ejecuta `uvicorn app.main:app --reload` dentro del directorio `backend/` después de instalar dependencias.

## Frontend
- SPA en React + Vite en `frontend/` con formulario para enviar facturas y panel de facturas recientes/estado del API.
- Ejecuta `npm install` y `npm run dev` dentro de `frontend/` (requiere Node 18+). Configura `VITE_API_BASE_URL` si el backend
  no está en `http://localhost:8000`.
