import logging
from typing import Any

from fastapi import HTTPException, Response
from sqlalchemy import Select, asc, desc, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Translation
from app.exceptions import DuplicateTranslationException
from app.models import (
    ExtraData,
    IncludeExtra,
    PaginatedResponse,
    TranslationCreate,
    TranslationRequest,
    TranslationResponse,
)
from app.paginator import Paginator
from app.translation import translate

logger = logging.getLogger(__name__)


class PaginateMixin:
    async def paginate(
        self, query: Select, page: int, per_page: int
    ) -> PaginatedResponse[Any]:
        paginator_class = self.get_paginator_class()  # type: ignore
        paginator = paginator_class(self.session, query, page, per_page)  # type: ignore
        return await paginator.get_response()


class TranslationService(PaginateMixin):
    paginator_class: type[Paginator] = Paginator

    def __init__(self, session: AsyncSession):
        self.session = session

    def get_paginator_class(self) -> type[Paginator]:
        return self.paginator_class or Paginator

    async def get_translation_by_word(
        self,
        word: str,
        target_lang: str,
    ) -> Translation | None:
        query = select(Translation).where(
            (Translation.word == word) & (Translation.target_lang == target_lang)
        )
        result = await self.session.execute(query)
        translation = result.scalars().first()
        return translation

    async def get_translations(
        self,
        page: int = 1,
        per_page: int = 10,
        sort_desc: bool = False,
        search: str = "",
        extra: IncludeExtra = IncludeExtra(),
    ) -> PaginatedResponse[dict]:
        query = select(Translation)

        if search:
            query = query.where(Translation.word.ilike(f"%{search}%"))

        if sort_desc:
            query = query.order_by(desc(Translation.word))
        else:
            query = query.order_by(asc(Translation.word))

        paginate = await self.paginate(query, page, per_page)
        include_extra_fields = extra.true_attributes

        # update paginate items and include only passed extras
        paginate.items = [
            {
                "word": item.word,
                "target_lang": item.target_lang,
                "source_lang": item.source_lang,
                "translated_word": item.translated_word,
                "pronunciation": item.pronunciation,
                "extra_data": ExtraData.from_orm(item).dict(
                    include=include_extra_fields, exclude_unset=True, exclude_none=True
                ),
            }
            for item in paginate.items
        ]
        return paginate

    async def create_translation(
        self, translation_data: TranslationResponse
    ) -> Translation:
        translation = Translation(**translation_data.dict())
        self.session.add(translation)
        try:
            await self.session.commit()
            return translation
        except IntegrityError as e:
            await self.session.rollback()
            message = f"The translation already exists: {str(e)}"
            logger.error(message)
            raise DuplicateTranslationException(message) from e

    async def get_or_create_translation(
        self, request: TranslationRequest
    ) -> TranslationCreate:
        # attempt to get translation from database
        translation = await self.get_translation_by_word(
            word=request.word,
            target_lang=request.target_lang,
        )
        if translation is None:
            # get & store translation from Google
            translation_data = translate(
                text=request.word,
                source_lang=request.source_lang,
                dest_lang=request.target_lang,
            )
            translation = await self.create_translation(translation_data)

        return TranslationCreate(
            id=int(translation.id),
            word=str(translation.word),
            pronunciation=translation.pronunciation,  # type: ignore
            translated_word=str(translation.translated_word),
            extra_data=ExtraData(**translation.extra_data),
            source_lang=str(translation.source_lang),
            target_lang=str(translation.target_lang),
        )

    async def delete_translation(self, request: TranslationRequest):
        translation = await self.get_translation_by_word(
            word=request.word,
            target_lang=request.target_lang,
        )
        if not translation:
            raise HTTPException(status_code=404, detail="Translation not found")

        await self.session.delete(translation)
        await self.session.commit()

        response = Response(status_code=204)
        return response
