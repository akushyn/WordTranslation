from typing import Generic, TypeVar
from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    word: str
    target_lang: str
    source_lang: str | None = None


class TranslationResponse(TranslationRequest):
    translated_word: str
    pronunciation: str | None = None
    extra_data: dict


class TranslationCreate(TranslationResponse):
    id: int


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    count: int = Field(description="Items count")
    page_num: int = Field(description="Page number")
    per_page: int = Field(description="Items per page")
    pages: int = Field(description="Pages count")
    items: list[T] = Field(description="Response Items")
    next: str | None
    previous: str | None
