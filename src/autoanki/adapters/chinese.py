from autoanki.adapters.base import LanguageAdapter
from autoanki.tokenizers import ChineseTokenizer


class ChineseAdapter(LanguageAdapter):
    def __init__(self, settings: dict = {}):
        self.include_pinyin = settings.get("include_pinyin", False)
        self.include_zhuyin = settings.get("include_zhuyin", False)
        self.include_part_of_speech = settings.get("include_part_of_speech", False)
        self.include_traditional = settings.get("include_traditional", False)
        self.include_audio = settings.get("include_traditional", False)
        self.word_frequency_filter = settings.get("word_frequency_filter", 0)
        self.set_hsk_filter = settings.get("set_hsk_filter", 0)

    def tokenize(self, text) -> list[str]:
        tokenizer = ChineseTokenizer()
        return tokenizer.tokenize(text)

    def store(self, tokens: list[str], group_name="default"):
        pass

    def lookup(self, token) -> dict:
        # TODO set up the database manager here
        return {}

    def available_settings(self) -> dict:
        return {
            "include_pinyin": {},
            "include_zhuyin": {},
            "include_part_of_speech": {},
            "include_traditional": {},
            "include_audio": {},
            "word_frequency_filter": {},
        }

    def settings(self):
        pass

    def get_note_fields(self, token) -> dict:
        entry = self.lookup(token)
        return {"front": entry["word"]}
        #'number_of_occurrences': 0,
        #'word': '',
        #'word_traditional': '',
        #'pinyin': '',
        #'pinyin_numbers': '',
        #'zhuyin': '',
        #'jyutping': '',
        #'part_of_speech': '',
        #'number_of_strokes': 0,
        #'sub_components': '',
        #'definition': '',
        #'frequency': 0,
        #'hsk_level': 0,
        #'tocfl_level': 0,
        #'audio_path': '',
        #'image_path': '',
        #'character_graphic': '',
        #'examples': [],

    def get_tokens_to_generate(self) -> dict:
        # TODO
        return {"中文": self.get_note_fields("中文")}
