import logging

from app.models import WordTranslationRequest, WordTranslationResponse
from googletrans import Translator  # type: ignore
from googletrans.models import Translated
from app.exceptions import TranslationException

_translator = Translator()
logger = logging.getLogger(__name__)


class TranslationHandler:
    def process(self, request: WordTranslationRequest) -> WordTranslationResponse:
        logger.info(f"Start word processing: {request.model_dump()}")

        translation = get_translation(
            text=request.word,
            source_lang=request.source_lang,
            dest_lang=request.target_lang,
        )

        return WordTranslationResponse(
            translated_word=translation.text,
            pronunciation=translation.pronunciation,
            definitions=translation.extra_data["definitions"],
            synonyms=translation.extra_data["synonyms"],
            examples=translation.extra_data["examples"],
            all_translations=translation.extra_data["all-translations"],
            source_lang=translation.src,
            target_lang=translation.dest,
            word=translation.origin,
        )


def get_translation(text: str, source_lang: str | None, dest_lang: str) -> Translated:
    logger.info(
        f"Call google translate API to get translation: "
        f"text={text}; source_lang={source_lang}; dest_lang={dest_lang}"
    )

    try:
        source_lang = source_lang or "auto"
        result = _translator.translate_legacy(text, src=source_lang, dest=dest_lang)
    except ValueError as e:
        message = f"Error occurred during translating text {text}: {str(e)}"
        logger.error(message)
        raise TranslationException(message)

    return result
