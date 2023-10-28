from sqlalchemy import Column, UniqueConstraint
from sqlalchemy import Integer, String
from sqlalchemy.dialects.postgresql import JSON
from app.db.base import Base
from sqlalchemy.ext.hybrid import hybrid_property


class Translation(Base):
    __tablename__ = "translations"
    __table_args__ = (
        UniqueConstraint(
            "word",
            "target_lang",
            name="uc_word_target_lang",
        ),
    )

    id = Column(Integer, autoincrement=True, primary_key=True)
    word = Column(String, index=True, nullable=False)
    translated_word = Column(String, index=True, nullable=False)
    pronunciation = Column(String)
    source_lang = Column(String)
    target_lang = Column(String, nullable=False)
    extra_data = Column(JSON, nullable=False, default=lambda: {})

    @hybrid_property
    def translation(self):
        return self.extra_data.get("translation")

    @hybrid_property
    def all_translations(self):
        return self.extra_data.get("all_translations")

    @hybrid_property
    def possible_translations(self):
        return self.extra_data.get("possible_translations")

    @hybrid_property
    def possible_mistakes(self):
        return self.extra_data.get("possible_mistakes")

    @hybrid_property
    def synonyms(self):
        return self.extra_data.get("synonyms")

    @hybrid_property
    def definitions(self):
        return self.extra_data.get("definitions")

    @hybrid_property
    def examples(self):
        return self.extra_data.get("examples")
