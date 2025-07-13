from autoanki.adapters.base import LanguageAdapter
from autoanki.tokenizers import ChineseTokenizer


class ChineseAdapter(LanguageAdapter):
    def __init__(self, settings):
        self.include_pinyin = settings.get("include_pinyin", False)
        self.include_zhuyin = settings.get("include_zhuyin", False)
        self.include_part_of_speech = settings.get("include_part_of_speech", False)
        self.include_traditional = settings.get("include_traditional", False)
        self.include_audio = settings.get("include_traditional", False)
        self.word_frequency_filter = settings.get("word_frequency_filter", 0)

    def set_hsk_filter():
        # TODO
        """
        `hsk_filter`: Float between 0 and 1. 1 being every word is included, 0 being none are included
        """
        pass

    def tokenize(self, text) -> list[str]:
        tokenizer = ChineseTokenizer()
        return tokenizer.tokenize(text)

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
        return {
            'front': entry['word']

        }


















