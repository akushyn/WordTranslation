from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .middlewares import request_object
from .models import PaginatedResponse


class Paginator:
    def __init__(self, session: AsyncSession, query: Select, page: int, per_page: int):
        self.session = session
        self.query = query
        self.page = page
        self.per_page = per_page
        self.limit = per_page
        self.offset = (page - 1) * per_page
        self.request = request_object.get()

        # computed later
        self.number_of_pages = 0
        self.total_count = 0
        self.next_page = ""
        self.previous_page = ""

    def _get_next_page(self) -> str | None:
        if self.page >= self.number_of_pages:
            return None
        url = self.request.url.include_query_params(page=self.page + 1)
        return str(url)

    def _get_previous_page(self) -> str | None:
        if self.page == 1 or self.page > self.number_of_pages + 1:
            return None
        url = self.request.url.include_query_params(page=self.page - 1)
        return str(url)

    async def get_response(self) -> PaginatedResponse:
        items_count = await self._get_total_count()
        pages_count = await self._get_number_of_pages(items_count)
        items = [
            item
            for item in await self.session.scalars(
                self.query.limit(self.limit).offset(self.offset)
            )
        ]

        return PaginatedResponse(
            page_num=self.page,
            per_page=self.per_page,
            count=items_count,
            pages=pages_count,
            next=self._get_next_page(),
            previous=self._get_previous_page(),
            items=items,
        )

    async def _get_number_of_pages(self, count: int) -> int:
        rest = count % self.per_page
        quotient = count // self.per_page
        return quotient if not rest else quotient + 1

    async def _get_total_count(self) -> int:
        count = await self.session.scalar(
            select(func.count()).select_from(self.query.subquery())
        )
        if count is None:
            count = 0

        self.total_count = count
        self.number_of_pages = await self._get_number_of_pages(count)
        return count
