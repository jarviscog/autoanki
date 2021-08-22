import book_to_word_list
import web_assests
import check_char_count
import os
import general_functions

if __name__ == "__main__":

    filename = "full_book_with_pinyin.txt"

    word_list_filename = os.path.splitext(filename)[0]
    word_list_filename = word_list_filename + book_to_word_list.NEW_FILE_EXTENTION

    if (not general_functions.file_exists(word_list_filename)):
        word_list_filename = book_to_word_list.convert(filename, sort_by_frequency=False, has_pinyin=True, write_frequency=True)

    web_assests.getDefinitions(word_list_filename)

