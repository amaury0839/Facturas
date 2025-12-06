"""Proxy module to expose the FastAPI app from the backend package.

Having this wrapper allows running ``uvicorn app.main:app`` from the
repository root without modifying the working directory or PYTHONPATH.
"""
from backend.app.main import app

__all__ = ["app"]
