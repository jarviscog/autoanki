from .Dictionary import Dictionary
from os import path
from pprint import pprint
import re
import logging

logger = logging.getLogger('autoanki.cedict')
logger.setLevel(logging.DEBUG)

PATH_TO_FILE = "./cedict_ts.u8"

class CEDictionary(Dictionary):

    def __init__(self):
        """Chinese to English Dictionary

        """
        pass


    def find_word(self, word: str) -> None | list[str]:

        if not path.isfile(PATH_TO_FILE):
            logger.critical("Could not open dictionary file")

        definitions = []
        valid_line = ""
        found_entry = False # There can be multiple definitions per word
        # TODO Some entries use a dot in the midde
        #   e.g. 哈利·波特
        #   this does not currently match
        # TODO This could be done faster

        with open(PATH_TO_FILE, "r") as dict_file:
            for line in dict_file:
                parts = line.split(" ")
                if word in [parts[0], parts[1]]:
                    definitions.append('/' + line.split('/', 1)[1].strip('\n'))
                    valid_line = line
                    found_entry = True
                # If we found a definition, and the current line doesn't match, exit
                if found_entry and word not in [parts[0], parts[1]]:
                    break
                
        if not valid_line:
            #logger.info("Entry not in dictionary")
            return None

        params = ["", "", "", "", "", "", "", "", ""]
        logger.debug(valid_line)

        #traditional_script = params[0]\n
        params[0] = valid_line.split(" ")[0] 

        
        #pinyin_numbers = params[3]\n
        m = re.compile(r"\[[^]]*\]")
        match = m.findall(valid_line)
        logger.debug(match)
        params[3] = match[0]


        #definition = params[7]\n
        def_param = ""
        for definition in definitions:
            def_param += definition
        params[7] = def_param 

        #word = params[8]
        params[8] = valid_line.split(" ")[1] 

        # pprint(params)

        return params


    def size(self):
        with open(PATH_TO_FILE,"r") as f:
            return len(f.readlines()) 




