from sqlalchemy import Column
from sqlalchemy import Integer
from app.db.base import Base


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, autoincrement=True, primary_key=True)
