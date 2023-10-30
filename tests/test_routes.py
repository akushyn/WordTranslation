from unittest.mock import AsyncMock, patch

import pytest

from app.models import TranslationRequest


@pytest.fixture
def mock_request():
    request = TranslationRequest(word="challenge", target_lang="ru", source_lang="en")
    return request


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
