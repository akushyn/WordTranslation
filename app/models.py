from pydantic import BaseModel


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
