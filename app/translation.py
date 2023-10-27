import logging
from app.models import TranslationResponse
from googletrans import Translator  # type: ignore
from app.exceptions import TranslationException
from app.settings import settings


_translator = Translator(
    service_urls=settings.googletrans_service_urls,
    raise_exception=settings.googletrans_raise_exception,
    proxies=settings.googletrans_proxies,
)

logger = logging.getLogger(__name__)


def translate(
    text: str, source_lang: str | None, dest_lang: str
) -> TranslationResponse:
    logger.info(
        f"Call google translate API to get translation: "
        f"text={text}; source_lang={source_lang}; dest_lang={dest_lang}"
    )
    source_lang = source_lang or "auto"
    try:
        translation = _translator.translate(text, src=source_lang, dest=dest_lang)
    except ValueError as e:
        message = f"Error occurred during translating text {text}: {str(e)}"
        logger.error(message)
        raise TranslationException(message)

    return TranslationResponse(
        translated_word=translation.text,
        pronunciation=translation.pronunciation,
        extra_data=translation.extra_data or {},
        source_lang=translation.src,
        target_lang=translation.dest,
        word=translation.origin,
    )
