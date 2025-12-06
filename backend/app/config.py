from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: Optional[str] = None
    telegram_webhook_secret: Optional[str] = None

    class Config:
        env_prefix = "FACTURAS_"
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
