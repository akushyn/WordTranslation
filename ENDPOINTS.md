# Word Translation Service API Endpoints

The following is the description and usage examples of the service endpoints.

## `GET /api/translations/word/`

**Endpoint description.** This endpoint gets or creates new word translation.

Query parameters description:

* `word` - (`string`) the word for translation.
* `target_lang` - (`string`) a target language code to translate.
* `source_lang` - (`string`) a source language code, auto detected, if not defined.

Example output (JSON):

```json
{
    "word": "challenge",
    "target_lang": "ru",
    "source_lang": "en",
    "translated_word": "испытание",
    "pronunciation": "ispytaniye",
    "extra_data": {
        "translation": [
            [
                "испытание",
                "challenge",
                null,
                null,
                10
            ],
            [
                null,
                null,
                "ispytaniye",
                "ˈCHalənj"
            ]
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
                    "опознавательные сигналы"
                ]
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
                    "давать отвод присяжным"
                ],
                ...
                "challenge",
                2
            ]
        ],
        "possible_translations": [
            [...]
        ],
        "possible_mistakes": null,
        "synonyms": [
            [
                "имя существительное",
                [
                    [
                        [
                            "dare",
                            "provocation",
                            "summons"
                        ],
                        "m_en_gbus0167500.006"
                    ],
                    [
                        [
                            "problem",
                            "difficult task",
                            "test",
                            "trial",
                            "trouble",
                            "bother",
                            "obstacle"
                        ],
                        "m_en_gbus0167500.009"
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
                            "ultimatum"
                        ],
                        "m_en_gbus0167500.012"
                    ]
                ],
                "challenge",
                1
            ]
        ],
        "definitions": [
            [
                "имя существительное",
                [
                    [
                        "a call to take part in a contest or competition, especially a duel.",
                        "m_en_gbus0167500.006",
                        "he accepted the challenge"
                    ],
                    [
                        "an objection or query as to the truth of something, often with an implicit demand for proof.",
                        "m_en_gbus0167500.012",
                        "a challenge to the legality of the order"
                    ],
                    [
                        "exposure of the immune system to pathogenic organisms or antigens.",
                        "m_en_gbus0167500.016",
                        "recently vaccinated calves should be protected from challenge",
                        [
                            null,
                            null,
                            [
                                "Medicine"
                            ]
                        ]
                    ]
                ],
                "challenge",
                1
            ]
        ],
        "examples": [
        ]
    },
    "id": 15
}
```

Output values description:

* `word` - Requested word for translation
* `target_lang` - The target language code.
* `source_lang` - The source language code of `word`
* `translated_word` - The translated word to `target_lang`.
* `pronunciation` - The pronunciation of `word`.
* `extra_data` - The additional translation information: `synonyms`, `definitions`, etc.


## `DELETE /api/translations/word/`

**Endpoint description.** Delete translation by specified `word` and `target_lang` code.

Query parameters description:

* `word` - (`string`) a word of translation to delete
* `target_lang` - (`string`) a target language code of word to delete.



## `GET /api/translations/`

**Endpoint description.** This endpoint returns paginated list of translations.

Query parameters description:

* `page` - (`int`) a page number to return
* `per_page` - (`int`) a count of items to return per page, configured in `settings.pagination_per_page`
* `search` - (`string`) Partial word filtering.
* `sort_desc` - (`bool`) Whether to sort descending, otherwise ascending, configured in `settings.pagination_sort_desc`
* `synonyms` - (`bool`) Whether to include `synonyms` for items in `extra_data`
* `definitions` - (`bool`) Whether to include `definitions` for items in `extra_data`
* `examples` - (`bool`) Whether to include `examples` for items in `extra_data`
* `all_translations` - (`bool`) Whether to include `all_translations` for items in `extra_data`
* `result` - (`bool`) Whether to include `result` for items in `extra_data`
* `translation` - (`bool`) Whether to include `translation` for items in `extra_data`
* `possible_translations` - (`bool`) Whether to include `possible_translations` for items in `extra_data`
* `possible_mistakes` - (`bool`) Whether to include `possible_mistakes` for items in `extra_data`

Example output (JSON):

```json
{
    "count": 15,
    "page_num": 1,
    "per_page": 10,
    "pages": 2,
    "items": [
        {
            "word": "challenge",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "испытание",
            "pronunciation": "ispytaniye",
            "extra_data": {}
        },
        {
            "word": "competition",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "соревнование",
            "pronunciation": "sorevnovaniye",
            "extra_data": {}
        },
        {
            "word": "door",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "дверь",
            "pronunciation": "dver'",
            "extra_data": {}
        },
        {
            "word": "holiday",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "праздничный день",
            "pronunciation": "prazdnichnyy den'",
            "extra_data": {}
        },
        {
            "word": "home",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "дом",
            "pronunciation": "dom",
            "extra_data": {}
        },
        {
            "word": "mistake",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "ошибка",
            "pronunciation": "oshibka",
            "extra_data": {}
        },
        {
            "word": "procrastination",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "прокрастинация",
            "pronunciation": "prokrastinatsiya",
            "extra_data": {}
        },
        {
            "word": "result",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "результат",
            "pronunciation": "rezul'tat",
            "extra_data": {}
        },
        {
            "word": "star",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "звезда",
            "pronunciation": "zvezda",
            "extra_data": {}
        },
        {
            "word": "success",
            "target_lang": "ru",
            "source_lang": "en",
            "translated_word": "успех",
            "pronunciation": "uspekh",
            "extra_data": {}
        }
    ],
    "next": "http://0.0.0.0:8000/api/translations?page=2",
    "previous": null
}
```

Output values description:

* `count` - The total count of translations
* `page_num` - The page number
* `per_page` - The count of items to return per page
* `pages` - The count of pages
* `items` - A list of `translation` object information
  * `word` - Requested word for translation
  * `target_lang` - The target language code.
  * `source_lang` - The source language code of `word`
  * `translated_word` - The translated word to `target_lang`.
  * `pronunciation` - The pronunciation of `word`.
  * `extra_data` - The additional translation information: `synonyms`, `definitions`, etc.

Output explanation:

The output represents paginated list of words translations, where `extra_data` by default is empty.
Response object sorted by `word`.


## `GET /api/translations/word/`

**Endpoint description.** This endpoint gets or creates new word translation.

Query parameters description:

* `word` - (`string`) the word for translation.
* `target_lang` - (`string`) a target language code to translate.
* `source_lang` - (`string`) a source language code, auto detected, if not defined.

Example output (JSON):

```json
{
    "word": "challenge",
    "target_lang": "ru",
    "source_lang": "en",
    "translated_word": "испытание",
    "pronunciation": "ispytaniye",
    "extra_data": {
        "translation": [
            [
                "испытание",
                "challenge",
                null,
                null,
                10
            ],
            [
                null,
                null,
                "ispytaniye",
                "ˈCHalənj"
            ]
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
                    "опознавательные сигналы"
                ]
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
                    "давать отвод присяжным"
                ],
                ...
                "challenge",
                2
            ]
        ],
        "possible_translations": [
            [...]
        ],
        "possible_mistakes": null,
        "synonyms": [
            [
                "имя существительное",
                [
                    [
                        [
                            "dare",
                            "provocation",
                            "summons"
                        ],
                        "m_en_gbus0167500.006"
                    ],
                    [
                        [
                            "problem",
                            "difficult task",
                            "test",
                            "trial",
                            "trouble",
                            "bother",
                            "obstacle"
                        ],
                        "m_en_gbus0167500.009"
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
                            "ultimatum"
                        ],
                        "m_en_gbus0167500.012"
                    ]
                ],
                "challenge",
                1
            ]
        ],
        "definitions": [
            [
                "имя существительное",
                [
                    [
                        "a call to take part in a contest or competition, especially a duel.",
                        "m_en_gbus0167500.006",
                        "he accepted the challenge"
                    ],
                    [
                        "an objection or query as to the truth of something, often with an implicit demand for proof.",
                        "m_en_gbus0167500.012",
                        "a challenge to the legality of the order"
                    ],
                    [
                        "exposure of the immune system to pathogenic organisms or antigens.",
                        "m_en_gbus0167500.016",
                        "recently vaccinated calves should be protected from challenge",
                        [
                            null,
                            null,
                            [
                                "Medicine"
                            ]
                        ]
                    ]
                ],
                "challenge",
                1
            ]
        ],
        "examples": [
        ]
    },
    "id": 15
}
```

## `GET /api/languages/`

**Endpoint description.** This endpoint gets a list of supported languages.

Example output (JSON):

```json
{
    "af": "afrikaans",
    "sq": "albanian",
    "am": "amharic",
    "ar": "arabic",
    "hy": "armenian",
    "az": "azerbaijani",
    "eu": "basque",
    "be": "belarusian",
    "bn": "bengali",
    "bs": "bosnian",
    "bg": "bulgarian",
    "ca": "catalan",
    "ceb": "cebuano",
    "ny": "chichewa",
    "zh-cn": "chinese (simplified)",
    "zh-tw": "chinese (traditional)",
    "co": "corsican",
    "hr": "croatian",
    "cs": "czech",
    "da": "danish",
    "nl": "dutch",
    "en": "english",
    "eo": "esperanto",
    "et": "estonian",
    "tl": "filipino",
    "fi": "finnish",
    "fr": "french",
    "fy": "frisian",
    "gl": "galician",
    "ka": "georgian",
    "de": "german",
    "el": "greek",
    "gu": "gujarati",
    "ht": "haitian creole",
    "ha": "hausa",
    "haw": "hawaiian",
    "iw": "hebrew",
    "he": "hebrew",
    "hi": "hindi",
    "hmn": "hmong",
    "hu": "hungarian",
    "is": "icelandic",
    "ig": "igbo",
    "id": "indonesian",
    "ga": "irish",
    "it": "italian",
    "ja": "japanese",
    "jw": "javanese",
    "kn": "kannada",
    "kk": "kazakh",
    "km": "khmer",
    "ko": "korean",
    "ku": "kurdish (kurmanji)",
    "ky": "kyrgyz",
    "lo": "lao",
    "la": "latin",
    "lv": "latvian",
    "lt": "lithuanian",
    "lb": "luxembourgish",
    "mk": "macedonian",
    "mg": "malagasy",
    "ms": "malay",
    "ml": "malayalam",
    "mt": "maltese",
    "mi": "maori",
    "mr": "marathi",
    "mn": "mongolian",
    "my": "myanmar (burmese)",
    "ne": "nepali",
    "no": "norwegian",
    "or": "odia",
    "ps": "pashto",
    "fa": "persian",
    "pl": "polish",
    "pt": "portuguese",
    "pa": "punjabi",
    "ro": "romanian",
    "ru": "russian",
    "sm": "samoan",
    "gd": "scots gaelic",
    "sr": "serbian",
    "st": "sesotho",
    "sn": "shona",
    "sd": "sindhi",
    "si": "sinhala",
    "sk": "slovak",
    "sl": "slovenian",
    "so": "somali",
    "es": "spanish",
    "su": "sundanese",
    "sw": "swahili",
    "sv": "swedish",
    "tg": "tajik",
    "ta": "tamil",
    "te": "telugu",
    "th": "thai",
    "tr": "turkish",
    "uk": "ukrainian",
    "ur": "urdu",
    "ug": "uyghur",
    "uz": "uzbek",
    "vi": "vietnamese",
    "cy": "welsh",
    "xh": "xhosa",
    "yi": "yiddish",
    "yo": "yoruba",
    "zu": "zulu"
}
```
