import logging
import time
import urllib

import requests
from bs4 import BeautifulSoup
import urllib.parse
import pinyin as pin_to_num

from .Dictionary import Dictionary

logger = logging.getLogger('autoanki')
# logger.setLevel()


class YellowBridgeDictionary(Dictionary):

    def __init__(self):
        pass

    def find_word(self, word, cache_number=None):
        '''
        Helper function for complete_unfinished_dictionary_records() Takes a word (one or more characters),
        finds them on YellowBridge, and adds them to the dictionary
        :param word: The word to find on YellowBridge.
        :param cache_number: The secondary page number for a word with multiple definitions. (See comments in body of
        function)
        :return:
        '''
        print(repr(word))
        if word == None or word == '':
            print("There is no page on Yellowbridge page for null")
            return

        urlx = "http://www.yellowbridge.com/chinese/dictionary.php?word="
        url = urlx + urllib.parse.quote(word)
        if cache_number is not None:
            url += "&cache=" + cache_number

        response = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'})
        yellowbridge_soup = BeautifulSoup(response.content, "html.parser")

        body = yellowbridge_soup.find(id='tabbody')
        main_data = yellowbridge_soup.find(id='mainData')
        # Some definitions will show up on the page differently because they have multiple meanings/pronunciations
        # e.g 了 could be le or liao.
        # These pages actually link to other pages with a different 'cache' number
        # Default 了 page:
        # https://www.yellowbridge.com/chinese/dictionary.php?word=%E4%BA%86
        # Page for le:
        # https://www.yellowbridge.com/chinese/dictionary.php?word=%E4%BA%86&cache=5114
        # Page for laio:
        # https://www.yellowbridge.com/chinese/dictionary.php?word=%E4%BA%86&cache=5115
        # This means that it would have to be possible to have multiple rows in the dictionary with the same word column,
        # which breaks other parts of the code.
        # For now, we just grab the first cache number and use that one. Maybe a v2 FEATURE will be able to have multiple
        # definitions for the same character, but that is not a priority currently
        if main_data:
            yellowbridge_contains_exact_definition = True
        else:
            yellowbridge_contains_exact_definition = False
        if yellowbridge_contains_exact_definition:
            definition = simplified_script = traditional_script = pinyin = pinyin_num = part_of_speech = hsk_level = top_level = composing_words = None
            main_data = main_data.find_all('tr')
            # Collect all necessary information from the page:
            for row in main_data:
                row_info_type = row.find('td').getText()
                row_info = row.find_all('td')[1].getText()
                # print(row_info_type + ":")
                # print(row_info)
                if row_info_type == "English Definition":
                    definition = row_info
                elif row_info_type == "Simplified Script":
                    simplified_script = row_info
                elif row_info_type == "Traditional Script":
                    traditional_script = row_info.split("P")[0]
                elif row_info_type == "Pinyin":
                    pinyin = row_info
                    pinyin_num = pin_to_num.get(word, format="numerical")
                elif row_info_type == "Part of Speech":
                    part_of_speech = row_info
                elif row_info_type == "Proficiency Test Level":
                    proficiency_level = row_info
                    if "HSK=" in proficiency_level:
                        hsk_level = proficiency_level.split("HSK=")[1].split(";")[0]
                    if "TOP=" in proficiency_level:
                        top_level = proficiency_level.split("TOP=")[1].split(";")[0]

            word_decomposition_soup = yellowbridge_soup.find(id='wordDecomp')
            if len(word) > 1:
                composing_words_list = word_decomposition_soup.find_all('tr')
                composing_words = ""
                for composing_word in composing_words_list:
                    composing_words += str(composing_word.find_all('td')[0].find('a').getText()) + ";"

            # This is all of the information that has been collected
            # print([definition, simplified_script, traditional_script,pinyin,pinyin_num, part_of_speech,hsk_level,top_level,composing_words])
            params = [traditional_script, part_of_speech, pinyin, pinyin_num,
                      composing_words, hsk_level, top_level, definition, word]
            # Add the information for this word to the database

            return params
        else:
            # print("This is not a definition page. getting all sub-pages")
            matching_results = yellowbridge_soup.find(id='multiRow')
            # Grab first row. This is usually the most common definition
            row = matching_results.find_all('tr')[0]
            # print(row.find('a'))
            href = str(row.find('a')['href'])
            # print(href)
            cache_number_from_href = href.split("word=")[1].split("&")[1].replace("cache=", "")

            return self.find_word(word, cache_number_from_href)

    def size(self):
        return 0

