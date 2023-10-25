from fastapi import APIRouter


router = APIRouter()


@router.get("/ping", include_in_schema=False)
async def pong():
    return {"ping": "pong!"}


@router.get("/words/id")
async def get_word_details(id: int):
    pass
