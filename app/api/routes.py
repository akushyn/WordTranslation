from app.paginator import Paginator
from app.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_session
from fastapi import Query
from app.models import (
    TranslationRequest,
    TranslationCreate,
    PaginatedResponse,
    TranslationResponse,
)
from app.services import TranslationService
from fastapi import APIRouter, Depends


router = APIRouter()


@router.get("/translations/word", response_model=TranslationCreate)
async def get_translation(
    request: TranslationRequest = Depends(),
    session: AsyncSession = Depends(get_session),
) -> TranslationCreate:
    service = TranslationService(session)
    response = await service.get_or_create_translation(request)
    return response


@router.delete("/translations/word")
async def delete_translation(
    request: TranslationRequest = Depends(),
    session: AsyncSession = Depends(get_session),
):
    service = TranslationService(session)
    response = await service.delete_translation(request)
    return response


@router.get(
    "/translations",
    response_model=PaginatedResponse[TranslationResponse],
)
async def get_translations(
    page: int = Query(1, ge=0),
    per_page: int = Query(
        settings.pagination_per_page, ge=0, le=settings.pagination_per_page_max
    ),
    sort_desc: bool = settings.pagination_sort_desc,
    search: str = Query(default=""),
    session: AsyncSession = Depends(get_session),
) -> PaginatedResponse[TranslationResponse]:
    service = TranslationService(session=session)
    service.paginator_class = Paginator

    return await service.get_translations(
        page=page,
        per_page=per_page,
        sort_desc=sort_desc,
        search=search,
    )
