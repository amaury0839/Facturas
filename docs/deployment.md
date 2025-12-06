# Manual de despliegue

Guía rápida para publicar el backend FastAPI de facturación 606/607.

## Requisitos
- Python 3.11+
- Acceso a shell Linux o contenedor con Git y systemd/pm2 (según preferencia)
- Credenciales de Telegram para notificaciones (token de bot y chat ID)

## Preparación del entorno
1. Clonar el repositorio y ubicarse en la carpeta `backend`.
2. Crear un entorno virtual y activar:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Definir variables de entorno en un archivo `.env` o en el servicio que uses para ejecutar el proceso:
   - `TELEGRAM_BOT_TOKEN`: token del bot de Telegram que enviará las notificaciones.
   - `TELEGRAM_CHAT_ID`: chat o canal (con el bot agregado) que recibirá el mensaje.

> Si no defines las variables de Telegram, el servicio seguirá funcionando pero no enviará alertas.

## Ejecución local (desarrollo)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Verifica el estado: `curl http://localhost:8000/health`
- Endpoints de ejemplo: `POST /invoices`, `GET /invoices`.

## Despliegue en producción
1. Ejecuta uvicorn con workers mediante `gunicorn` o `uvicorn` directamente. Ejemplo simple con `systemd`:
   ```ini
   [Unit]
   Description=Facturas 606/607 API
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/ruta/a/Facturas/backend
   Environment="TELEGRAM_BOT_TOKEN=..." "TELEGRAM_CHAT_ID=..."
   ExecStart=/ruta/a/Facturas/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
2. Recarga y habilita el servicio:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now facturas.service
   ```
3. Coloca un proxy reverso (Nginx/Traefik) para TLS y balanceo si es necesario.

## Base de datos
- Por defecto se usa SQLite (`data.db` en la carpeta raíz). Para entornos multiusuario, reemplaza la URL `DATABASE_URL` en `app/database.py` por PostgreSQL o MySQL.
- Ejecuta la app una vez para que las tablas se creen automáticamente.

## Notificaciones de Telegram
- Las notificaciones se disparan al crear una factura. Incluyen origen, tipo de operación, NCF y datos básicos.
- Para enviarlas asegúrate de definir `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` en el entorno del proceso.

## Troubleshooting
- **No envía notificaciones:** revisa que el bot esté en el chat y que el `chat_id` corresponda al chat/canal correcto.
- **Permisos de archivo SQLite:** verifica que el usuario del proceso tenga permisos de escritura en la carpeta `backend`.
- **Errores 404 en facturas:** comprueba que el `invoice_id` exista y que la base de datos sea la correcta.

## Checklist operativo para despliegues
1. **Preparar el entorno:** confirma que estás en una rama estable (p. ej., `main`) y que las variables de entorno/secrets (API keys, base de datos) están configuradas en el servidor.
2. **Verificar calidad:** ejecuta pruebas automáticas y herramientas de linting; revisa métricas de performance si aplica.
3. **Construir artefactos:** genera el build (frontend/backend) y contenedores si se usan; etiqueta la versión con un número o fecha.
4. **Ensayar en staging:** despliega en un entorno de prueba similar a producción y valida funciones clave y seguridad.
5. **Aprobar y programar:** solicita el visto bueno de QA/Producto y agenda una ventana de despliegue comunicando a usuarios si es necesario.
6. **Desplegar a producción:** ejecuta el despliegue (CI/CD o manual) siguiendo un checklist y monitorea logs, métricas y alertas.
7. **Post-despliegue:** revisa errores, rendimiento y feedback de usuarios; documenta cambios y aprendizajes para la siguiente iteración.
