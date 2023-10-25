import logging

from googletrans import Translator  # type: ignore

from app.exceptions import TranslationException

_translator = Translator()
logger = logging.getLogger(__name__)


def translate(text: str, source_lang: str, dest_lang: str | None = None) -> str:
    try:
        translation = _translator.translate(text, src=source_lang, dest=dest_lang)
    except ValueError as e:
        message = f"Error occurred during translating text {text}: {str(e)}"
        logger.error(message)
        raise TranslationException(message)

    return translation
