import pytest
from pydantic.error_wrappers import ValidationError

from app.models import (
    ExtraData,
    GoogleTranslationResult,
    IncludeExtra,
    TranslationCreate,
    TranslationRequest,
)
from tests.conftest import faker


@pytest.fixture
def translation_request():
    request = TranslationRequest(word="challenge", target_lang="ru", source_lang="en")
    return request


@pytest.fixture
def extra_data():
    return {
        "translation": [
            ["испытание", "challenge", 10],
        ],
        "all_translations": [
            [
                "имя существительное",
                [
                    "вызов",
                    "проблема",
                    "сложная задача",
                    "отвод",
                    "сомнение",
                    "оклик",
                    "вызов на дуэль",
                    "опознавательные сигналы",
                ],
                "challenge",
                1,
            ],
            [
                "глагол",
                [
                    "оспаривать",
                    "бросать вызов",
                    "подвергать сомнению",
                    "вызывать",
                    "требовать",
                    "окликать",
                    "спрашивать пропуск",
                    "спрашивать пароль",
                    "сомневаться",
                    "отрицать",
                    "давать отвод присяжным",
                ],
                "challenge",
                2,
            ],
        ],
        "possible_translations": [],
        "possible_mistakes": None,
        "synonyms": [
            [
                "имя существительное",
                [
                    [["dare", "provocation", "summons"], "m_en_gbus0167500.006"],
                    [
                        [
                            "problem",
                            "difficult task",
                            "test",
                            "trial",
                            "trouble",
                            "bother",
                            "obstacle",
                        ],
                        "m_en_gbus0167500.009",
                    ],
                    [
                        [
                            "confrontation with",
                            "dispute with",
                            "stand against",
                            "test of",
                            "opposition",
                            "disagreement with",
                            "questioning of",
                            "defiance",
                            "ultimatum",
                        ],
                        "m_en_gbus0167500.012",
                    ],
                ],
                "challenge",
                1,
            ],
        ],
        "definitions": [
            [
                "имя существительное",
                [
                    [
                        "a call to take part in a contest or competition, "
                        "especially a duel.",
                        "m_en_gbus0167500.006",
                        "he accepted the challenge",
                    ],
                    [
                        "an objection or query as to the truth of something, "
                        "often with an implicit demand for proof.",
                        "m_en_gbus0167500.012",
                        "a challenge to the legality of the order",
                    ],
                    [
                        "exposure of the immune system to pathogenic organisms "
                        "or antigens.",
                        "m_en_gbus0167500.016",
                        "recently vaccinated calves should be protected from challenge",
                    ],
                ],
                "challenge",
                1,
            ],
        ],
        "examples": [],
    }


def test_translation_request():
    request = TranslationRequest(word="challenge", target_lang="ru")
    assert request.word == "challenge"
    assert request.target_lang == "ru"
    assert request.source_lang is None


def test_translation_request_word_raise_validation_errors():
    with pytest.raises(ValidationError) as exc_info:
        TranslationRequest(word="Wrong Challenge", target_lang="ru")

    error = exc_info.value.errors()[0]
    assert exc_info.type is ValidationError
    assert str(error["msg"]) == "Multiple words translation is not supported"
    assert str(error["type"]) == "value_error"


def test_translation_request_target_lang_raise_validation_errors():
    with pytest.raises(ValidationError) as exc_info:
        TranslationRequest(word=faker.word(), target_lang="wrong_lang")

    error = exc_info.value.errors()[0]
    assert exc_info.type is ValidationError
    assert str(error["msg"]) == (
        "Invalid target language: wrong_lang. "
        "Must be one of [af, sq, am, ar, hy, az, eu, be, bn, bs, bg, ca, ceb, ny, "
        "zh-cn, zh-tw, co, hr, cs, da, nl, en, eo, et, tl, fi, fr, fy, gl, ka, de, el, "
        "gu, ht, ha, haw, iw, he, hi, hmn, hu, is, ig, id, ga, it, ja, jw, kn, kk, "
        "km, ko, ku, ky, lo, la, lv, lt, lb, mk, mg, ms, ml, mt, mi, mr, mn, my, ne, "
        "no, or, ps, fa, pl, pt, pa, ro, ru, sm, gd, sr, st, sn, sd, si, sk, sl, so, "
        "es, su, sw, sv, tg, ta, te, th, tr, uk, ur, ug, uz, vi, cy, xh, yi, yo, zu]"
    )
    assert str(error["type"]) == "value_error"


def test_extra_data_defaults():
    extra_data = ExtraData()
    assert extra_data.translation is None
    assert extra_data.all_translations is None
    assert extra_data.possible_translations is None
    assert extra_data.synonyms is None
    assert extra_data.definitions is None
    assert extra_data.examples is None
    assert extra_data.Config.orm_mode is True


def test_extra_data(extra_data):
    result = ExtraData(**extra_data)
    assert result.translation == [["испытание", "challenge", 10]]
    assert result.synonyms == [
        [
            "имя существительное",
            [
                [["dare", "provocation", "summons"], "m_en_gbus0167500.006"],
                [
                    [
                        "problem",
                        "difficult task",
                        "test",
                        "trial",
                        "trouble",
                        "bother",
                        "obstacle",
                    ],
                    "m_en_gbus0167500.009",
                ],
                [
                    [
                        "confrontation with",
                        "dispute with",
                        "stand against",
                        "test of",
                        "opposition",
                        "disagreement with",
                        "questioning of",
                        "defiance",
                        "ultimatum",
                    ],
                    "m_en_gbus0167500.012",
                ],
            ],
            "challenge",
            1,
        ]
    ]
    assert result.definitions == [
        [
            "имя существительное",
            [
                [
                    "a call to take part in a contest or competition, "
                    "especially a duel.",
                    "m_en_gbus0167500.006",
                    "he accepted the challenge",
                ],
                [
                    "an objection or query as to the truth of something, often with an "
                    "implicit demand for proof.",
                    "m_en_gbus0167500.012",
                    "a challenge to the legality of the order",
                ],
                [
                    "exposure of the immune system to "
                    "pathogenic organisms or antigens.",
                    "m_en_gbus0167500.016",
                    "recently vaccinated calves should be protected from challenge",
                ],
            ],
            "challenge",
            1,
        ]
    ]


def test_include_extra():
    include_extra = IncludeExtra()

    assert include_extra.result is False
    assert include_extra.translation is False
    assert include_extra.all_translations is False
    assert include_extra.possible_translations is False
    assert include_extra.possible_mistakes is False
    assert include_extra.synonyms is False
    assert include_extra.definitions is False
    assert include_extra.examples is False

    assert include_extra.true_attributes == set()


def test_include_extra_true_attributes():
    include_extra = IncludeExtra(synonyms=True, definitions=True)
    assert include_extra.result is False
    assert include_extra.translation is False
    assert include_extra.all_translations is False
    assert include_extra.possible_translations is False
    assert include_extra.possible_mistakes is False
    assert include_extra.synonyms is True
    assert include_extra.definitions is True
    assert include_extra.examples is False

    assert include_extra.true_attributes == {"synonyms", "definitions"}


def test_translation_response(translation_request, extra_data):
    translated_word = "испытание"
    extra_data = ExtraData.from_orm(extra_data)

    translation_response = GoogleTranslationResult(
        translated_word=translated_word,
        extra_data=extra_data,
        **translation_request.dict(),
    )
    assert translation_response.pronunciation is None
    assert translation_response.extra_data.dict() == extra_data
    assert translation_response.word == translation_request.word
    assert translation_response.translated_word == translated_word
    assert translation_response.source_lang == translation_request.source_lang
    assert translation_response.target_lang == translation_request.target_lang


def test_translation_create(translation_request, extra_data):
    translation_id = faker.random_int()
    translated_word = faker.word()
    extra_data = ExtraData.from_orm(extra_data)

    translation_response = TranslationCreate(
        id=translation_id,
        translated_word=translated_word,
        extra_data=extra_data,
        **translation_request.dict(),
    )
    assert translation_response.pronunciation is None
    assert translation_response.extra_data.dict() == extra_data
    assert translation_response.word == translation_request.word
    assert translation_response.translated_word == translated_word
    assert translation_response.source_lang == translation_request.source_lang
    assert translation_response.target_lang == translation_request.target_lang
    assert translation_response.id == translation_id
