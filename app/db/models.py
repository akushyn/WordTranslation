from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSON
from app.db.base import Base


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, autoincrement=True, primary_key=True)
    word = Column(String, unique=True, index=True, nullable=False)
    translated_word = Column(String, index=True, nullable=False)
    pronunciation = Column(String)
    source_lang = Column(String)
    target_lang = Column(String, nullable=False)
    extra_data = Column(JSON, nullable=False, default=lambda: {})
