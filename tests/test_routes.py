from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import Response

from app.models import ExtraData, PaginatedResponse, TranslationRequest
from app.settings import settings


@pytest.fixture
def mock_request():
    request = TranslationRequest(word="challenge", target_lang="ru", source_lang="en")
    return request


@pytest.fixture
def mock_translation(faker):
    translation = MagicMock()
    translation.id = faker.random_int()
    translation.word = faker.word()
    translation.translated_word = faker.word()
    translation.pronunciation = faker.word()
    translation.source_lang = "en"
    translation.target_lang = "ru"
    translation.extra_data = ExtraData()

    # include hybrid properties
    translation.translation = None
    translation.all_translations = None
    translation.possible_translations = None
    translation.possible_mistakes = None
    translation.synonyms = None
    translation.definitions = None
    translation.examples = None

    return translation


@pytest.mark.real
def test_get_languages(client):
    response = client.get("/api/languages")

    assert response.status_code == 200
    assert len(response.json()) == 107
    assert response.json() == {
        "af": "afrikaans",
        "am": "amharic",
        "ar": "arabic",
        "az": "azerbaijani",
        "be": "belarusian",
        "bg": "bulgarian",
        "bn": "bengali",
        "bs": "bosnian",
        "ca": "catalan",
        "ceb": "cebuano",
        "co": "corsican",
        "cs": "czech",
        "cy": "welsh",
        "da": "danish",
        "de": "german",
        "el": "greek",
        "en": "english",
        "eo": "esperanto",
        "es": "spanish",
        "et": "estonian",
        "eu": "basque",
        "fa": "persian",
        "fi": "finnish",
        "fr": "french",
        "fy": "frisian",
        "ga": "irish",
        "gd": "scots gaelic",
        "gl": "galician",
        "gu": "gujarati",
        "ha": "hausa",
        "haw": "hawaiian",
        "he": "hebrew",
        "hi": "hindi",
        "hmn": "hmong",
        "hr": "croatian",
        "ht": "haitian creole",
        "hu": "hungarian",
        "hy": "armenian",
        "id": "indonesian",
        "ig": "igbo",
        "is": "icelandic",
        "it": "italian",
        "iw": "hebrew",
        "ja": "japanese",
        "jw": "javanese",
        "ka": "georgian",
        "kk": "kazakh",
        "km": "khmer",
        "kn": "kannada",
        "ko": "korean",
        "ku": "kurdish (kurmanji)",
        "ky": "kyrgyz",
        "la": "latin",
        "lb": "luxembourgish",
        "lo": "lao",
        "lt": "lithuanian",
        "lv": "latvian",
        "mg": "malagasy",
        "mi": "maori",
        "mk": "macedonian",
        "ml": "malayalam",
        "mn": "mongolian",
        "mr": "marathi",
        "ms": "malay",
        "mt": "maltese",
        "my": "myanmar (burmese)",
        "ne": "nepali",
        "nl": "dutch",
        "no": "norwegian",
        "ny": "chichewa",
        "or": "odia",
        "pa": "punjabi",
        "pl": "polish",
        "ps": "pashto",
        "pt": "portuguese",
        "ro": "romanian",
        "ru": "russian",
        "sd": "sindhi",
        "si": "sinhala",
        "sk": "slovak",
        "sl": "slovenian",
        "sm": "samoan",
        "sn": "shona",
        "so": "somali",
        "sq": "albanian",
        "sr": "serbian",
        "st": "sesotho",
        "su": "sundanese",
        "sv": "swedish",
        "sw": "swahili",
        "ta": "tamil",
        "te": "telugu",
        "tg": "tajik",
        "th": "thai",
        "tl": "filipino",
        "tr": "turkish",
        "ug": "uyghur",
        "uk": "ukrainian",
        "ur": "urdu",
        "uz": "uzbek",
        "vi": "vietnamese",
        "xh": "xhosa",
        "yi": "yiddish",
        "yo": "yoruba",
        "zh-cn": "chinese (simplified)",
        "zh-tw": "chinese (traditional)",
        "zu": "zulu",
    }


@patch(
    "app.api.routes.TranslationService.get_or_create_translation",
    new_callable=AsyncMock,
)
def test_get_translation(mock_get_or_create_translation, mock_request, client):
    mock_get_or_create_translation.return_value = {
        "id": 123,
        "word": "challenge",
        "translated_word": "испытание",
        "target_lang": "ru",
        "source_lang": "en",
        "extra_data": mock_request.dict(),
    }

    response = client.get("/api/translations/word/", params=mock_request.dict())

    assert response.status_code == 200
    assert response.json() == {
        "word": "challenge",
        "target_lang": "ru",
        "source_lang": "en",
        "translated_word": "испытание",
        "pronunciation": None,
        "extra_data": {
            "translation": None,
            "all_translations": None,
            "possible_translations": None,
            "possible_mistakes": None,
            "synonyms": None,
            "definitions": None,
            "examples": None,
        },
        "id": 123,
    }
    mock_get_or_create_translation.assert_called_once_with(mock_request)


@patch(
    "app.api.routes.TranslationService.delete_translation",
    new_callable=AsyncMock,
)
def test_delete_translation(mock_delete_translation, mock_request, client):
    mock_delete_translation.return_value = Response(status_code=204)

    response = client.delete("/api/translations/word/", params=mock_request.dict())

    assert response.status_code == 204
    assert response.text == ""
    mock_delete_translation.assert_called_once_with(mock_request)


@patch("app.api.routes.TranslationService.paginate", new_callable=AsyncMock)
def test_get_translations(mock_paginate, client, mock_translation, faker):
    mock_next = faker.url()
    mock_previous = faker.url()
    translations_count = 3
    mock_translations = [mock_translation for _ in range(translations_count)]

    mock_paginate.return_value = PaginatedResponse(
        count=len(mock_translations),
        page_num=1,
        per_page=settings.pagination_per_page,
        pages=1,
        items=mock_translations,
        next=mock_next,
        previous=mock_previous,
    )

    response = client.get("/api/translations/")
    response_payload = response.json()

    assert response.status_code == 200
    assert len(response_payload["items"]) == translations_count
    assert response_payload["count"] == translations_count
    assert response_payload["next"] == mock_next
    assert response_payload["previous"] == mock_previous
    assert response_payload["pages"] == 1
    assert response_payload["per_page"] == settings.pagination_per_page
