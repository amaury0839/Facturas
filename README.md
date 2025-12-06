# Facturas

Diseño y lineamientos para una aplicación que gestiona facturas de compras (606) y ventas (607) para DGII en República Dominicana.

Consulta `docs/architecture.md` para la arquitectura, modelo de datos, flujos, validaciones y pseudocódigo clave.

## Backend
- Backend inicial en FastAPI en `backend/` con modelos SQLModel para facturas, totales y pagos.
- Ejecuta `uvicorn app.main:app --reload` dentro del directorio `backend/` después de instalar dependencias.
