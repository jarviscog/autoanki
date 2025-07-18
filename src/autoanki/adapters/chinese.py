from autoanki.adapters.base import LanguageAdapter
from autoanki.database.chinese import ChineseDatabaseManager
from autoanki.tokenizer import ChineseTokenizer


class ChineseAdapter(LanguageAdapter):
    def __init__(self, settings: dict = {}):
        self.settings = {}

        self.settings["include_traditional"] = settings.get("include_traditional", True)

        # Pronunciation
        self.settings["include_pinyin"] = settings.get("include_pinyin", False)
        self.settings["include_zhuyin"] = settings.get("include_zhuyin", False)

        # POS
        self.settings["include_part_of_speech"] = settings.get(
            "include_part_of_speech", False
        )
        self.settings["tone_colors"] = settings.get("tone_colors", False)

        # Filters
        self.settings["word_frequency_filter"] = settings.get(
            "word_frequency_filter", 0
        )
        self.settings["set_hsk_filter"] = settings.get("set_hsk_filter", 0)

        # self.database_manager = ChineseDatabaseManager(debug_level=20)
        self.test_dict = {}

    def tokenize(self, text) -> list[str]:
        tokenizer = ChineseTokenizer()
        tokens = tokenizer.tokenize(text)
        return tokens

    def store(self, tokens: list[str], group_name="default"):
        for token in tokens:
            self.test_dict[token] = {
                "word": token,
                "word_traditional": token,
                "group": group_name,
            }

    def lookup(self, token) -> dict | None:
        # TODO set up the database manager here
        res = self.test_dict.get(token, None)
        return res

    def get_number_of_entries(self) -> int:
        return len(self.test_dict)

    def get_groups(self) -> list[str]:
        groups = []
        for word in self.test_dict.keys():
            word_dict = self.test_dict.get(word, {})
            group = word_dict.get("group", None)
            groups.append(group)
        return list(set(groups))
        # return self.database_manager.books

    def available_settings(self) -> dict:
        return list(self.settings.keys())

    def get_settings(self) -> dict:
        return self.settings

    def get_note_fields(self, token) -> dict:
        entry = self.lookup(token)
        if not entry:
            return {}

        if self.settings["tone_colors"]:
            entry[
                "word"
            ] = f"""<span style="color:red">{entry.get("word", "")}</span>"""

        # if traditional == simplified, replace with dash
        word_traditional = ""
        raw_word_traditional = entry.get("word_traditional", "")
        for i in range(len(token)):
            if token[i] == raw_word_traditional[i]:
                word_traditional += "-"
            else:
                word_traditional += raw_word_traditional[i]
        entry["word_traditional"] = word_traditional

        return {
            "word": entry["word"],
            "word_alternate": entry.get("word_traditional", ""),
            "pronunciation": entry.get("pinyin", ""),
            "pronunciation_alternate": entry.get("zhuyin", ""),
            "part_of_speech": entry.get("part_of_speech", ""),
            "definition": entry.get("definition", ""),
        }
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

        return_dict = {}
        for key, val in self.test_dict.items():
            return_dict[key] = self.get_note_fields(key)
        return return_dict
