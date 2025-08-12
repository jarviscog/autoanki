from dataclasses import dataclass

@dataclass
class LookupResult:
    word: str
    lang: str
    definition: str| None = None
    ipa: str | None = None
    part_of_speech: str | None = None
    #'examples': [],
    #'frequency': 0,
    #'audio_path': '',
    #'image_path': '',
    #'character_graphic': '',

@dataclass
class ChineseLookupResult(LookupResult):
    traditional: str | None = None

    pinyin: str | None = None
    #'pinyin_numbers': '',
    zhuyin: str | None = None
    jyutping: str | None = None
    #'number_of_strokes': 0,
    #'sub_components': '',

    hsk_level: str | None = None
    #'tocfl_level': 0,

@dataclass
class FrenchLookupResult(LookupResult):
    gender: str | None = None
    conjugations: str | None = None



