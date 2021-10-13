import web_assets
import os
import book_to_word_list
import card_generator
import general_functions

if __name__ == "__main__":

    filename = "maze_runner.txt"

    # word_list_freq_filename = os.path.splitext(filename)[0]
    # word_list_filename = word_list_freq_filename + "_word_list_freq.txt"
    #
    # if (not general_functions.file_exists(word_list_filename)):
    #     print("Getting word list")
    word_list_freq_filename = book_to_word_list.convert('test.txt', sort_by_frequency=False, write_frequency=True, extension='_word_list.txt')
    #     word_list_filename = book_to_word_list.convert(filename, sort_by_frequency=False, has_pinyin=True, write_frequency=False, extension='_word_list.txt')
    #
    # # print("Getting pinyin")
    # word_list_w_pinyin = web_assets.getPinyin(word_list_filename)
    # word_list_w_pinyin_numbers = web_assets.getPinyinNumbers(word_list_w_pinyin)
    #
    # web_assets.getDefinitions(word_list_w_pinyin_numbers, 'maze_runner_definitions.txt', 500)
    # web_assets.getDefinitions('maze_runner_definition.txt', 'maze_runner_definition1.txt', 50)

    card_generator.generate_file('Maze Runner','maze_runner_definition1.txt')

    # web_assets.getAssets(word_list_w_pinyin_numbers)
