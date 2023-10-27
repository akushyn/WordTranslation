from pydantic import BaseModel


class WordTranslationRequest(BaseModel):
    word: str
    target_lang: str
    source_lang: str | None = None


class WordTranslationResponse(WordTranslationRequest):
    translated_word: str
    pronunciation: str | None = None
    possible_translations: list = []
    synonyms: list = []
    definitions: list = []
    examples: list = []
