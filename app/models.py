from typing import Generic, TypeVar
from pydantic import BaseModel, Field, ConfigDict


class TranslationRequest(BaseModel):
    word: str
    target_lang: str
    source_lang: str | None = None


class ExtraData(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    translation: list | None = None
    all_translations: list | None = None
    possible_translations: list | None = None
    possible_mistakes: list | None = None
    synonyms: list | None = None
    definitions: list | None = None
    examples: list | None = None


class IncludeExtra(BaseModel):
    result: bool = False
    translation: bool = False
    all_translations: bool = False
    possible_translations: bool = False
    possible_mistakes: bool = False
    synonyms: bool = False
    definitions: bool = False
    examples: bool = False

    @property
    def true_attributes(self) -> set:
        true_attributes = set(
            attr for attr, value in self.model_dump().items() if value
        )
        return true_attributes


class TranslationResponse(TranslationRequest):
    translated_word: str
    pronunciation: str | None = None
    extra_data: ExtraData


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
