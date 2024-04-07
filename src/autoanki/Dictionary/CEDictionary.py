from .Dictionary import Dictionary
from os import path
import logging
import pinyin

import jieba
import jieba.posseg as pseg
import chinese_converter

PATH_TO_FILE = path.join(path.dirname(__file__), 'cedict_ts.u8')

#   Use the lookup table here: https://github.com/fxsjy/jieba
POS_LUT = {
    'n':'noun',
    'nt':'noun',
    'nrt':'noun',
    'ORG':'noun',
    'nr':'noun',
    'PER':'noun',
    'ns':'noun',
    'nw':'noun',
    'nz':'noun',
    'f':'noun',
    's':'noun',
    'an':'noun',
    't':'time',
    'TIME':'time',
    'p':'adposition',
    'r':'pronoun',
    'q':'quantifier',
    'm':'quantifier',
    'v':'verb',
    'vd':'verb',
    'vn':'verb',
    'a':'adjective',
    'ad':'adverb',
    'd':'adverb',
    'c':'conjunction',
    'u':'particle',
    'vn':'other',
    'xc':'other',
    'x':'other',
    'w':'puncuation',
}

class CEDictionary(Dictionary):

    def __init__(self, debug_level):
        """Chinese to English Dictionary

        """
        self.logger = logging.getLogger('autoanki.cedict')
        self.logger.setLevel(debug_level)
        self.logger.info("Loading Chinese Dictionary")
        self.dict = self._parse_file()
        self.logger.info("Done!")
        
        pass

    def _parse_file(self) -> dict[str, dict]:
        self.logger.info("Parsing file...")
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
                if line[0] == '#':
                    continue
                parts = line.split(" ")
                trad_word = parts[0]
                current_word = parts[1]

                definition = line[line.find("]")+2:]

                if current_word != last_word:
                    # self.logger.debug(f"Creating entry: {current_word}")
                    definitions[current_word] = {
                        'trad_word': "", 
                        'pinyin_numbers':"", 
                        'definition':"", 
                        'pinyin':""
                    }
                
                # These only need to be done the first time the word is seen
                if last_word != current_word:
                    definitions[current_word]['trad_word'] = trad_word
                    definitions[current_word]['pinyin'] = pinyin.get(current_word)
                    definitions[current_word]['pinyin_numbers'] = pinyin.get(current_word, format="numerical")


                definitions[current_word]['definition'] += '<br>' + definition 
                last_word = current_word

        for key, _ in definitions.items():
            definitions[key]['definition'].strip('\n')
        return definitions


    def find_word(self, word: str) -> None | list[str]:
        """
        Find a word in the dictionary. This can be simplified, or traditional
        `return` Paramaters that get passed to the database
        """
        
        # Convert the word to simplified if needed
        word = chinese_converter.to_simplified(word)

        if word in self.dict:
            """
            traditional_script = params[0]\n
            word_type = params[1]\n
            pinyin = params[2]\n
            pinyin_numbers = params[3]\n
            sub_components = params[4]\n
            hsk_level = params[5]\n
            top_level = params[6]\n
            definition = params[7]\n
            word = params[8]
            """
            params = ["", "", "", "", "", "", "", "", ""]

            slice = next(pseg.cut(word))
            part_of_speech = POS_LUT.get(slice.flag)
            if part_of_speech != None:
                params[1] = part_of_speech

            params[0] = self.dict[word]['trad_word'] 
            params[2] = self.dict[word]['pinyin'] 
            params[3] = self.dict[word]['pinyin_numbers'] 
            params[7] = self.dict[word]['definition'] 
            self.logger.debug(f"Word: {word}")
            params[8] = word
            return params
        else:
            return None 


    def size(self):
        with open(PATH_TO_FILE,"r") as f:
            return len(f.readlines()) 




