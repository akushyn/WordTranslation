import pytest

from app.models import TranslationResponse
from app.translation import translate


@pytest.mark.real
def test_translate(client):
    word = "challenge"
    target_lang = "ru"
    expected_pronunciation = "ispytaniye"
    expected_translated_word = "испытание"
    expected_source_lang = "en"

    result = translate(text=word, source_lang=None, dest_lang="ru")

    assert isinstance(result, TranslationResponse)
    assert result.word == word
    assert result.pronunciation == expected_pronunciation
    assert result.translated_word == expected_translated_word
    assert result.source_lang == expected_source_lang
    assert result.target_lang == target_lang
