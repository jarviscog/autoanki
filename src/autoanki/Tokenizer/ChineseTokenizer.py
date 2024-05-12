import logging

import jieba
logging.getLogger("jieba").setLevel(logging.WARNING)
import chinese_converter
from string import punctuation

from autoanki.Dictionary.CEDictionary import CEDictionary

# TODO Is there a way to do this in a smarter way? Maybe check if the characters are in a certian UTF-8 block?
PUNCTUATION = """
+,;:'()[]{}&*^%$#@!◇♦•·■◎∞=™©×
"""
CHINESE_PUNC = "！？｡。．.…、＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏  ① ② ③ ④ ⑽ "

# TODO: This can be extened and implemented
OTHER = "ｗ９ｌｉｔｂｎｅｐｈⅠ Ⅱ Ⅲ Ⅳ "

# TODO Remove straight numbers and english words

class ChineseTokenizer():

    def __init__(self, debug_level=20, dictionary=None):
        self.logger = logging.getLogger('autoanki.dbmngr')
        self.logger.setLevel(debug_level)

        # Currently, each element tokenized will be checked against the dictionary, 
        #   and shortented if there is not a match
        # TODO It's silly how much processing power this might use in worst-case. 
        #   Can we improve on this?
        if dictionary:
            self.dictionary = dictionary
        else:
            self.dictionary = CEDictionary(debug_level=20)

    def tokenize(self, line:str) -> None | list[str]:
        
        # TODO jieba has more features that we should take advantage of to get better tokenizing
        dirty_words = jieba.lcut(line)
        clean_words = []
        self.logger.debug("Dirty words:")
        self.logger.debug(dirty_words)
        for word in dirty_words:
            word = word.strip('\n')
            if not word:
                continue
            # Convert the word to simplified if needed
            word = chinese_converter.to_simplified(word)
            if len(word) == 1:
                if word in PUNCTUATION:
                    continue
                if word in CHINESE_PUNC:
                    continue
                if word in OTHER:
                    continue

            # If there is a definition in the dictionary, skip any more processing
            if not word:
                continue
            if self.dictionary.find_word(word):
                clean_words.append(word)
                continue


            # Try tokenizing again?
            subwords = jieba.lcut(word)
            if len(subwords) > 1:
                for subword in subwords:
                    clean_words.append(subword)
                continue

            # Remove all ascii
            new_word = ''.join(i for i in word if ord(i)>128)
            # if word != new_word:
                # self.logger.info(f"{word} -> {new_word}", )
            word = new_word
            if not word:
                continue
            if self.dictionary.find_word(word):
                clean_words.append(word)
                continue

            word = self.remove_modifiers(word)
            if not word:
                continue
            if self.dictionary.find_word(word):
                clean_words.append(word)
                continue

            word = self.remove_numbers(word)
            if not word:
                continue
            if self.dictionary.find_word(word):
                clean_words.append(word)
                continue

            # Repeated characters (always?) contain the same meaning as one, just varied slightly
            # 人人 = everyone
            if len(word) == 2 and word[0] == word[1]:
                word = word[0]
            if not word:
                continue
            if self.dictionary.find_word(word):
                clean_words.append(word)
                continue

            # TODO 2 repeated, 1?
            #   点点头
            #   长长的
            # TODO 的 at the end?
            # TODO 2 repeated, 2 repeated?
            #   起起伏伏
            # TODO Some gramatical patterns?
            # 在。。。上

            if len(word) == 2:
                clean_words.append(word[0])
                clean_words.append(word[1])
                continue

            if len(word) == 3:
                clean_words.append(word[0])
                clean_words.append(word[1])
                clean_words.append(word[2])
                continue

            if len(word) == 4:
                if self.dictionary.find_word(word[0:1]):
                    clean_words.append(word[0:1])
                else:
                    clean_words.append(word[0])
                    clean_words.append(word[1])

                if self.dictionary.find_word(word[2:3]):
                    clean_words.append(word[2:3])
                else:
                    clean_words.append(word[2])
                    clean_words.append(word[3])
                continue

            if len(word) == 5:
                clean_words.append(word[0])
                clean_words.append(word[1])
                clean_words.append(word[2])
                clean_words.append(word[3])
                clean_words.append(word[4])
                continue

            clean_words.append(word)

        if clean_words:
            self.logger.debug("Clean words")
            self.logger.debug(clean_words)
        return clean_words 


    def remove_numbers(self, word:str):
        # Remove all numbers from the front
        # Lots of the words follow the following format:
        #   Number + Subject
        CHINESE_NUMBERS = "第一二两三四五五六七八九十百千万满"
        old_word = "" 
        temp_word = word
        while old_word != temp_word:
            old_word = temp_word 
            if len(temp_word) == 0:
                break
            if temp_word[0] in CHINESE_NUMBERS:
                temp_word = temp_word[1:]
        return temp_word

    def remove_modifiers(self, word:str):
        stripped_word = word.lstrip('小')
        stripped_word = stripped_word.lstrip('大')
        stripped_word = stripped_word.lstrip('这')
        stripped_word = stripped_word.lstrip('那')
        stripped_word = stripped_word.lstrip('不')
        stripped_word = stripped_word.lstrip('几')
        stripped_word = stripped_word.lstrip('无')
        stripped_word = stripped_word.lstrip('没')
        stripped_word = stripped_word.lstrip('全')
        stripped_word = stripped_word.lstrip('上')
        stripped_word = stripped_word.lstrip('下')
        stripped_word = stripped_word.lstrip('太')
        stripped_word = stripped_word.lstrip('一个')
        return stripped_word


