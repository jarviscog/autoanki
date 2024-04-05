from .Dictionary import Dictionary
from os import path
import re
import logging
from pprint import pprint

PATH_TO_FILE = path.join(path.dirname(__file__), 'cedict_ts.u8')

class CEDictionary(Dictionary):

    def __init__(self, debug_level):
        """Chinese to English Dictionary

        """
        self.logger = logging.getLogger('autoanki.cedict')
        self.logger.setLevel(debug_level)
        self.dict = self._parse_file()
        
        pass

    def _parse_file(self) -> dict[str, dict]:
        self.logger.info("Parsing dict file...")
        if not path.isfile(PATH_TO_FILE):
            self.logger.critical("Could not open dictionary file")

        # TODO Some entries use a dot in the midde
        #   e.g. 哈利·波特
        #   this does not currently match
        definitions = {}
        last_word = "~~"
        current_word = ""

        with open(PATH_TO_FILE, "r") as dict_file:
            for line in dict_file:
                if line[0] == '#':
                    continue
                parts = line.split(" ")
                trad_word = parts[0]
                current_word = parts[1]
                
                m = re.compile(r"\[[^]]*\]")
                match = m.findall(line)
                # self.logger.debug(match)
                pinyin_numbers = match[0]

                definition = line[line.find("]")+2:]

                if current_word != last_word:
                    # self.logger.debug(f"Creating entry: {current_word}")
                    definitions[current_word] = {'trad_word': "", 'pinyin_numbers':"", 'definition':""}
                
                # self.logger.debug(f"Word: {current_word}")
                # self.logger.debug(f"Trad: {trad_word}")
                # self.logger.debug(f"PinYin: {pinyin_numbers}")
                # self.logger.debug(f"DEF: {definition}")
                definitions[current_word]['trad_word'] = trad_word
                definitions[current_word]['pinyin_numbers'] += pinyin_numbers 
                definitions[current_word]['definition'] += definition.strip("\n") 

                last_word = current_word

        self.logger.info("Done!")
        for key, value in definitions.items():
            print(key, '->', value)
        return definitions


    def find_word(self, word: str) -> None | list[str]:

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
            params[0] = self.dict[word]['trad_word'] 
            params[3] = self.dict[word]['pinyin_numbers'] 
            params[7] = self.dict[word]['definition'] 
            params[8] = word
            return params
        else:
            return None 


    def size(self):
        with open(PATH_TO_FILE,"r") as f:
            return len(f.readlines()) 




