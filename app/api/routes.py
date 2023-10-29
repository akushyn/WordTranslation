from fastapi import APIRouter, Depends, HTTPException, Query
from googletrans import LANGUAGES  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_session
from app.exceptions import DuplicateTranslationException, TranslationException
from app.models import (
    IncludeExtra,
    PaginatedResponse,
    TranslationCreate,
    TranslationRequest,
)
from app.services import TranslationService
from app.settings import settings

router = APIRouter()


@router.get("/translations/word/", response_model=TranslationCreate)
async def get_translation(
    request: TranslationRequest | None = None,
    session: AsyncSession | None = None,
) -> TranslationCreate:
    request = request or Depends()
    session = session or Depends(get_session)

    service = TranslationService(session)
    try:
        response = await service.get_or_create_translation(request)
        return response
    except (TranslationException, DuplicateTranslationException) as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete("/translations/word/")
async def delete_translation(
    request: TranslationRequest | None = None,
    session: AsyncSession | None = None,
):
    request = request or Depends()
    session = session or Depends(get_session)

    service = TranslationService(session)
    response = await service.delete_translation(request)
    return response


@router.get(
    "/translations/",
    response_model=PaginatedResponse[dict],
)
async def get_translations(
    page: int = Query(1, ge=0),
    per_page: int = Query(
        settings.pagination_per_page, ge=0, le=settings.pagination_per_page_max
    ),
    sort_desc: bool = settings.pagination_sort_desc,
    search: str = Query(default=""),
    include_extra: IncludeExtra | None = None,
    session: AsyncSession | None = None,
) -> PaginatedResponse[dict]:
    include_extra = include_extra or Depends()
    session = session or Depends(get_session)

    service = TranslationService(session=session)
    response = await service.get_translations(
        page=page,
        per_page=per_page,
        sort_desc=sort_desc,
        search=search,
        extra=include_extra,
    )
    return response


@router.get("/languages/")
async def get_languages() -> dict:
    return LANGUAGES
