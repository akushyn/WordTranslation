from typing import Generic, TypeVar

from googletrans import LANGUAGES  # type: ignore
from pydantic import BaseModel, validator

from app.enums import TranslationStatus


class TranslationRequest(BaseModel):
    word: str
    target_lang: str
    source_lang: str | None = None

    @validator("target_lang")
    def validate_target_lang(cls, value):
        if value not in LANGUAGES.keys():
            raise ValueError(
                f"Invalid target language: {value}. "
                f"Must be one of [{', '.join(LANGUAGES.keys())}]"
            )
        return value

    @validator("word")
    def validate_word(cls, value):
        if len(value.split()) > 1:
            raise ValueError("Multiple words translation is not supported")
        return value


class BatchTranslationRequest(BaseModel):
    blocks: list[TranslationRequest]


class ExtraData(BaseModel):
    translation: list | None = None
    all_translations: list | None = None
    possible_translations: list | None = None
    possible_mistakes: list | None = None
    synonyms: list | None = None
    definitions: list | None = None
    examples: list | None = None

    class Config:
        orm_mode = True


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
        true_attributes = set(attr for attr, value in self.dict().items() if value)
        return true_attributes


class GoogleTranslationResult(TranslationRequest):
    translated_word: str
    pronunciation: str | None = None
    extra_data: ExtraData


class TranslationCreate(GoogleTranslationResult):
    id: int


class TranslationSuccessResponse(BaseModel):
    status: str = TranslationStatus.success.value
    result: TranslationCreate


class TranslationFailResponse(BaseModel):
    status: str = TranslationStatus.fail.value
    message: str


class BatchTranslationResponse(BaseModel):
    results: list[TranslationSuccessResponse]


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    page_num: int
    per_page: int
    pages: int
    items: list[T]
    next: str | None
    previous: str | None
