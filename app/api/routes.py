import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query
from googletrans import LANGUAGES  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_session
from app.enums import TranslationStatus
from app.exceptions import (
    DuplicateTranslationException,
    TranslationException,
    TranslationNotFoundException,
)
from app.models import (
    BatchTranslationRequest,
    BatchTranslationResponse,
    IncludeExtra,
    PaginatedResponse,
    TranslationFailResponse,
    TranslationRequest,
    TranslationSuccessResponse,
)
from app.services import TranslationService
from app.settings import settings

router = APIRouter()


async def process_translation_request(request: TranslationRequest):
    try:
        async with get_session() as session:
            service = TranslationService(session)
            result = await service.get_or_create_translation(request)
            return TranslationSuccessResponse(
                status=TranslationStatus.success.value, result=result
            )
    except (TranslationException, DuplicateTranslationException) as e:
        return TranslationFailResponse(message=str(e))


@router.get("/translations/word/", response_model=TranslationSuccessResponse)
async def get_translation(
    request: TranslationRequest = Depends(),
) -> TranslationSuccessResponse:
    response = await get_batch_translation(
        batch_request=BatchTranslationRequest(blocks=[request])
    )
    return response.results[0]


@router.post("/translations/words/", response_model=BatchTranslationResponse)
async def get_batch_translation(
    batch_request: BatchTranslationRequest,
) -> BatchTranslationResponse:
    tasks = []

    # create tasks for processing each word
    for word_block in batch_request.blocks:
        task = asyncio.create_task(process_translation_request(word_block))
        tasks.append(task)

    # concurrently execute tasks
    results = await asyncio.gather(*tasks)
    return BatchTranslationResponse(results=results)


@router.delete("/translations/word/")
async def delete_translation(
    request: TranslationRequest = Depends(),
    session: AsyncSession = Depends(get_session),
):
    service = TranslationService(session)
    try:
        response = await service.delete_translation(request)
    except TranslationNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

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
    include_extra: IncludeExtra = Depends(),
) -> PaginatedResponse[dict]:
    async with get_session() as session:
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
