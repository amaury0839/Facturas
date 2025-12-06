"""Root-level application proxy for uvicorn.

This package forwards imports to the backend implementation so the app can
be launched from the repository root with ``uvicorn app.main:app``.
"""
from backend.app.main import app  # re-export FastAPI instance

__all__ = ["app"]
