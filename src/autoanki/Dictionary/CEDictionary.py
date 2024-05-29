from os import path
import logging

import pinyin
import jieba

logging.getLogger("jieba").setLevel(logging.WARNING)
import jieba.posseg as pseg
import chinese_converter
from wordfreq import word_frequency

from autoanki.Dictionary.Dictionary import Dictionary

PATH_TO_FILE = path.join(path.dirname(__file__), "cedict_ts.u8")

# Use the lookup table here: https://github.com/fxsjy/jieba
NOUN = [
    "n",
    "nt",
    "nrt",
    "ORG",
    "nr",
    "PER",
    "ns",
    "nw",
    "nz",
    "f",
    "s",
    "an",
    "zg",
    "j",
]
TIME = ["t", "TIME", "tg", "g"]
ADPOSITION = ["p"]
PRONOUN = ["r", "rz", "rg"]
QUANTIFIER = ["q", "m"]
VERB = ["v", "vd", "vn", "e", "vg", "h"]
ADVERB = ["ad", "d", "aq", "df"]
OTHER = ["vn", "xc", "x"]
ADJECTIVE = ["a", "b", "ng", "ag"]
CONJUNCTION = ["c"]
PARTICLE = ["y", "u", "uj", "uz", "ul", "uv", "ud", "ug"]
PUNCTUATION = ["w"]
IDIOM = ["i", "l"]
SUFFIX = ["k"]
OTHER = ["z", "o", "x"]


class CEDictionary(Dictionary):
    def __init__(self, debug_level):
        """Chinese to English Dictionary
        Parser for the CC-CEDICT Dictionary:
            https://www.mdbg.net/chinese/dictionary?page=cedict
        This is a file containing 122,839 entries
        """
        self.logger = logging.getLogger("autoanki.cedict")
        self.logger.setLevel(debug_level)
        self.logger.info("Loading Chinese Dictionary (CEDictionary)")
        self.dict = self._parse_file()
        self.logger.debug("Done!")

        pass

    def _parse_file(self) -> dict[str, dict]:
        """Parse dictionary file on load
        `return` A dictionary of the information, the key being the Chinese word
        """
        self.logger.debug("Parsing CE-DICT file...")
        if not path.isfile(PATH_TO_FILE):
            self.logger.critical("Could not open dictionary file")

        # TODO Some entries use a dot in the midde
        #   e.g. 哈利·波特
        #   this does not currently match
        definitions = {}
        last_word = "~"
        current_word = ""

        with open(PATH_TO_FILE, "r") as dict_file:
            for line in dict_file:
                if line[0] == "#":
                    continue
                parts = line.split(" ")
                trad_word = parts[0]
                current_word = parts[1]

                definition = line[line.find("]") + 2 :]

                if current_word != last_word:
                    # self.logger.debug(f"Creating entry: {current_word}")
                    definitions[current_word] = {
                        "trad_word": "",
                        "pinyin_numbers": "",
                        "definition": "",
                        "pinyin": "",
                        "frequency": "",
                    }

                # These only need to be done the first time the word is seen
                if last_word != current_word:
                    definitions[current_word]["traditional_word"] = trad_word
                    definitions[current_word]["pinyin"] = pinyin.get(current_word)
                    definitions[current_word]["pinyin_numbers"] = pinyin.get(
                        current_word, format="numerical"
                    )
                    definitions[current_word]["frequency"] = str(
                        100 * word_frequency(current_word, "zh")
                    )
                    slice = next(pseg.cut(current_word))
                    definitions[current_word][
                        "part_of_speech"
                    ] = self.get_part_of_speech(current_word, slice.flag)

                definitions[current_word]["definition"] += "<br>" + definition
                last_word = current_word

        for key, _ in definitions.items():
            definitions[key]["definition"].strip("\n")
            definitions[key]["definition"] = definitions[key]["definition"].lstrip(
                "<br>"
            )
            definitions[key]["definition"] = definitions[key]["definition"].lstrip("/")

            definitions[key]["definition"] = definitions[key]["definition"].rstrip("\n")
            definitions[key]["definition"] = definitions[key]["definition"].rstrip("/")
            # self.logger.info('[' + definitions[key]['definition'] + ']')
        return definitions

    def find_word(self, word: str) -> None | dict[str, str]:
        """
        Find a word in the dictionary. This can be simplified, or traditional
        `return` Paramaters that get passed to the database
        """
        # Convert the word to simplified if needed
        # TODO: This should happen during load, not runtime
        word = chinese_converter.to_simplified(word)
        # self.logger.info(f"[{word}] [{word in self.dict}]")
        word_found = self.dict.get(word)
        if not word_found:
            return None

        params = {}

        params["word"] = word
        params["word_traditional"] = word_found["traditional_word"]
        params["pinyin"] = word_found["pinyin"]
        params["pinyin_numbers"] = word_found["pinyin_numbers"]
        params["zhuyin"] = None
        params["jyutping"] = None
        params["part_of_speech"] = word_found["part_of_speech"]
        params["number_of_strokes"] = None
        params["sub_components"] = None
        params["definition"] = word_found["definition"]
        params["frequency"] = word_found["frequency"]
        params["HSK_level"] = None
        params["tocfl_level"] = None
        params["audio_path"] = None
        params["image_path"] = None
        params["character_graphic"] = None
        params["examples"] = None

        # self.logger.debug(f"Word: {word}")
        return params

    def size(self):
        with open(PATH_TO_FILE, "r") as f:
            return len(f.readlines())

    def get_part_of_speech(self, word: str, code: str) -> str:
        if code in NOUN:
            return "noun"
        if code in TIME:
            return "time"
        if code in ADPOSITION:
            return "adposition"
        if code in PRONOUN:
            return "pronoun"
        if code in QUANTIFIER:
            return "quantifier"
        if code in VERB:
            return "verb"
        if code in ADVERB:
            return "adverb"
        if code in OTHER:
            return "other"
        if code in ADJECTIVE:
            return "adjective"
        if code in CONJUNCTION:
            return "conjunction"
        if code in PARTICLE:
            return "particle"
        if code in PUNCTUATION:
            return "punctuation"
        if code in IDIOM:
            return "idiom"
        if code in PARTICLE:
            return "particle"
        if code in OTHER:
            return "other"
        if code in SUFFIX:
            return "suffix"

        self.logger.warning(f"Part of speech code not covered: {word}:{code}")
        return "other"
