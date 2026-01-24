# Instructivo rápido para probar Facturas

Sigue estos pasos cortos (todo en español) para levantar el backend y frontend localmente y validar que todo responde.

## 1) Requisitos
- Python 3.11+
- Node.js 18+ y npm
- `git`

## 2) Levantar el backend (FastAPI)
1. Abre una terminal y entra al backend:
   ```bash
   cd backend
   ```
2. Crea y activa un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instala dependencias y arranca el servidor en modo recarga:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
4. Prueba que está vivo desde otra terminal:
   ```bash
   curl http://localhost:8000/health
   ```
   Si responde `{ "status": "ok" }`, el backend está listo.

## 3) Consultar facturas sin usar el API
1. Con el backend corriendo, abre la base de datos local:
   ```bash
   sqlite3 backend/data.db
   ```
2. Ejecuta una consulta directa para ver las facturas:
   ```sql
   SELECT id, tipo_operacion, tipo_documento, ncf, fecha_comprobante, validation_status
   FROM invoices
   ORDER BY id DESC
   LIMIT 10;
   ```
3. Si ya cargaste facturas desde el frontend o Telegram, deberían aparecer aquí.

## 4) Levantar el frontend (React + Vite)
1. Abre otra terminal (deja el backend activo) y entra al frontend:
   ```bash
   cd frontend
   ```
2. Instala dependencias y arranca en modo desarrollo:
   ```bash
   npm install
   npm run dev
   ```
3. Si el backend no está en `http://localhost:8000`, define `VITE_API_BASE_URL` antes de `npm run dev`.
4. Abre el navegador en la URL que muestre Vite (por defecto http://localhost:5173) y envía la factura desde el formulario.
5. En el panel deberías ver la factura recién creada y el estado del API en verde.

## 5) Detener servicios
- Detén FastAPI con `Ctrl+C` en la terminal del backend.
- Detén Vite con `Ctrl+C` en la terminal del frontend.

¡Listo! Con estos pasos ya comprobaste que el API y la SPA funcionan en tu máquina.
