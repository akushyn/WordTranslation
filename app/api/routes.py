from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session

from app.models import TranslationRequest, TranslationCreate
from app.services import TranslationService
from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/ping", include_in_schema=False)
async def pong():
    return {"ping": "pong!"}


@router.get("/translations/word", response_model=TranslationCreate)
async def get_translation(
    request: TranslationRequest = Depends(),
    session: AsyncSession = Depends(get_session),
) -> TranslationCreate:
    service = TranslationService(session)
    response = await service.get_or_create_translation(request)
    return response
