import book_to_word_list
import web_assests
import os
import general_functions
import card_generator
if __name__ == "__main__":

    # filename = "maze_runner_pinyin.txt"
    #
    # word_list_freq_filename = os.path.splitext(filename)[0]
    # word_list_filename = word_list_freq_filename + "_word_list_freq.txt"
    #
    # if (not general_functions.file_exists(word_list_filename)):
    #     print("Getting word list")
    #     word_list_freq_filename = book_to_word_list.convert(filename, sort_by_frequency=False, has_pinyin=True, write_frequency=True, extention='_word_list_freq.txt')
    #     word_list_filename = book_to_word_list.convert(filename, sort_by_frequency=False, has_pinyin=True, write_frequency=False, extention='_word_list.txt')
    #
    # # print("Getting pinyin")
    # word_list_w_pinyin = web_assests.getPinyin(word_list_filename)
    # word_list_w_pinyin_numbers = web_assests.getPinyinNumbers(word_list_w_pinyin)
    #
    # web_assests.getDefinitions(word_list_w_pinyin_numbers, 'maze_runner_definitions.txt', 500)




    card_generator.createTestCard()





    # web_assests.getAssets(word_list_w_pinyin_numbers)
