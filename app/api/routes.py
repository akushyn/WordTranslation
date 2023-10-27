from app.models import WordTranslationRequest, WordTranslationResponse
from fastapi import APIRouter, Depends
from app.translation import TranslationHandler


router = APIRouter()


@router.get("/ping", include_in_schema=False)
async def pong():
    return {"ping": "pong!"}


@router.get("/translations/word", response_model=WordTranslationResponse)
async def get_translation(
    request: WordTranslationRequest = Depends(),
) -> WordTranslationResponse:
    handler = TranslationHandler()
    response = handler.process(request)
    return response
