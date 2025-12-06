from typing import Optional

from pydantic import BaseModel, Field


class TelegramUser(BaseModel):
    id: int
    is_bot: bool
    first_name: Optional[str] = None
    username: Optional[str] = None


class TelegramChat(BaseModel):
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None


class TelegramDocument(BaseModel):
    file_id: str
    file_unique_id: Optional[str] = None
    file_name: Optional[str] = Field(default=None, alias="file_name")
    mime_type: Optional[str] = Field(default=None, alias="mime_type")
    file_size: Optional[int] = Field(default=None, alias="file_size")

    class Config:
        allow_population_by_field_name = True


class TelegramMessage(BaseModel):
    message_id: int
    date: Optional[int] = None
    chat: TelegramChat
    from_: Optional[TelegramUser] = Field(default=None, alias="from")
    text: Optional[str] = None
    caption: Optional[str] = None
    document: Optional[TelegramDocument] = None

    class Config:
        allow_population_by_field_name = True


class TelegramUpdate(BaseModel):
    update_id: int
    message: Optional[TelegramMessage] = None

    @property
    def effective_chat_id(self) -> Optional[int]:
        if self.message:
            return self.message.chat.id
        return None

    @property
    def summary_text(self) -> str:
        if not self.message:
            return "Mensaje vacío"

        if self.message.text:
            return self.message.text

        if self.message.caption:
            return self.message.caption

        if self.message.document:
            return f"Archivo: {self.message.document.file_name or 'sin nombre'}"

        return "Mensaje sin texto"


class TelegramWebhookResponse(BaseModel):
    ok: bool
    message: str
