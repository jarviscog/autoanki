import math
import general_functions
from general_functions import GARBAGE_SENTENCES
import os
import time
import sqlite3
from os.path import isfile, join
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pinyin as pin_to_num
from pathlib import Path
from DatabaseManager.BookCleaner import BookCleaner, is_bookpath


def is_database(database_name):
    try:
        if database_name.split(".")[1] != "db":
            return 0
        if not os.path.exists(database_name):
            return 0

        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        # This will fail if dictionary table does not exist
        cursor.execute("SELECT word FROM dictionary")
    except:
        return 0
    return 1

def is_valid_database_filename(filename : str):

    if not general_functions.is_valid_filename(filename):
        return 0
    if(filename.split('.')[-1] != 'db'):
        return 0
    return 1


def create_autoanki_database(database_name):
    if not is_database(database_name):
        print("Creating database: " + database_name)

        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS dictionary(
        word_id INTEGER PRIMARY KEY AUTOINCREMENT,
        word VARCHAR(255) NOT NULL UNIQUE,
        word_traditional VARCHAR(255),
        word_type VARCHAR(255),
        pinyin VARCHAR(255),
        pinyin_numbers VARCHAR(255),
        number_of_strokes INTEGER,
        sub_components VARCHAR(255),
        frequency FLOAT,
        hsk_level VARCHAR(255),
        top_level VARCHAR(255),
        audio_path VARCHAR(255),
        image_path VARCHAR(255),
        definition VARCHAR(255)
)""")

    else:
        print(f"The database {database_name} already exists. No need to create it")


class DatabaseManager:

    def __init__(self, database_name):

        self.database_name = database_name
        self.book_list = []
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()

    def add_book_from_directory(self, bookpath):
        # TODO Add book from directory
        # 1 - Make a BookCleaner to clean book
        if not is_bookpath(bookpath):
            print("Unable to find path to book. Quitting")
            return 0
        else:
            book_cleaner = BookCleaner(bookpath)
            book_cleaner.clean()
        # 3 - Add the cleaned book to the database
        self._add_cleaned_book_to_database(bookpath)

    def _add_pinyin_pages_to_book_table(self, bookpath):
        """
        A helper function to take all of the cleaned files and add them to the database as a book table
        :param bookpath: the filepath to the book
        :return:
        """
        # print("Adding pinyin pages to database...")

        pinyin_pages_directory = str(Path(bookpath)) + "\\" + "pinyin_pages"

        book_table_name = bookpath.split("/")[-2]

        self.cursor.execute(f''' CREATE TABLE IF NOT EXISTS {book_table_name} (
                    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word VARCHAR(255) NOT NULL UNIQUE,
                    number_of_appearances INT,
                    CONSTRAINT UQ_word_pinyin UNIQUE(word)
                )''')

        filenames_to_add = [f for f in os.listdir(pinyin_pages_directory) if
                            isfile(join(pinyin_pages_directory, f))]
        number_of_words_added, number_of_words_not_added = 0, 0
        number_of_appearances_dict = {}

        for filename_to_add in filenames_to_add:
            valid_rows_num, invalid_rows_num = 0, 0

            file_to_add_length = general_functions.file_len(pinyin_pages_directory + "\\" + filename_to_add)
            page = open(pinyin_pages_directory + "\\" + filename_to_add, "r", encoding="utf-8")
            for i in range(math.ceil(file_to_add_length / 2)):
                pinyin = page.readline() \
                    .replace("\n", "") \
                    .replace("。", "") \
                    .replace("，", " ") \
                    .replace("   ", " ") \
                    .replace("    ", " ") \
                    .replace("  ", " ") \
                    .split(" ")
                chars = page.readline() \
                    .replace("\n", "") \
                    .replace("。", "") \
                    .replace("，", " ") \
                    .replace("   ", " ") \
                    .replace("  ", " ") \
                    .split(" ")

                if len(chars) == len(pinyin):
                    valid_rows_num += 1
                    for j in range(len(chars)):
                        if chars[j] in number_of_appearances_dict:
                            number_of_appearances_dict[str(chars[j])] += 1
                        else:
                            number_of_appearances_dict[chars[j]] = 1
                            number_of_words_added += 1
                else:
                    invalid_rows_num += 1
                    for j in range(len(chars)):
                        number_of_words_not_added += 1

            print("For: " + filename_to_add)
            print("Valid lines: " + str(valid_rows_num))
            print("Invalid lines: " + str(invalid_rows_num))
            print("")
        # TODO This is a bit too slow, and not scalable. Fix this.
        print("Adding files to book table...this may take a while...")
        # Take the number_of_appearances_dict dict and add all items to the database
        # print("Number of words in number_of_appearances_dict: " + str(len(number_of_appearances_dict)))
        for word, appearances in number_of_appearances_dict.items():
            if word not in GARBAGE_SENTENCES:
                self.cursor.execute(f"SELECT * FROM {book_table_name} WHERE word = ?", [word])
                response = self.cursor.fetchall()
                if len(response) > 0:
                    # If a word has been found in the dictionary, add
                    # print("Word " + word + " is already in db")
                    response_word_id, response_word, response_word_appearances = response[0]
                    combined_appearances = appearances + response_word_appearances
                    self.cursor.execute(
                        f"UPDATE {book_table_name} SET number_of_appearances = ? WHERE word = ?",
                        [combined_appearances, word])
                    self.connection.commit()
                else:
                    # print("Word " + word + " is not in db")
                    self.cursor.execute(
                        f"INSERT INTO {book_table_name} (word, number_of_appearances) VALUES (?, ?)",
                        [word, appearances])
                    self.connection.commit()

        print("---Done adding new table to database!---")
        print("---Words added: " + str(number_of_words_added) + "---")
        print("---Words not added: " + str(number_of_words_not_added) + "---")
        # TODO Fix the terrible book coverage from parsing sentences in chapter files (about 10% right now)
        print("---Book coverage: " + "{0:.2f}".format(
            (number_of_words_added / (number_of_words_added + number_of_words_not_added)) * 100)
              + "%---")

    def _add_book_table_to_definitions_table(self, bookpath):
        """
        Takes all rows from the book table and adds them to the definitions table if they are not there already
        :return:
        """
        database_table_name = bookpath.split("/")[-2]
        print("Adding rows from " + database_table_name + " to dictionary...")
        self.cursor.execute(f"SELECT * FROM {database_table_name} WHERE word IS NOT NULL")
        book_table_rows = self.cursor.fetchall()
        for book_table_row in book_table_rows:
            book_table_id, book_table_word, book_table_number_of_appearances = book_table_row
            print("Current row: " + str(book_table_id) + " " + str(book_table_word) + " " + str(
                book_table_number_of_appearances))
            self.cursor.execute("SELECT * FROM dictionary WHERE word = ?", [book_table_word])
            response = self.cursor.fetchall()
            print("Response: " + str(response))
            print("Response length: " + str(len(response)))
            if len(response) > 0:
                print("Entry already present")
                print(response)
            else:
                print("Entry not present. Adding...")
                self.cursor.execute(f"INSERT INTO dictionary (word) VALUES (?)", [book_table_word])
                # self.cursor.execute(f"INSERT INTO dictionary (word) VALUES (\"他\")")
                self.connection.commit()

    def _add_cleaned_book_to_database(self, bookpath):
        """
        Helper function to add a cleaned book to the database. This will both create the table for the book,
        as well as add all new words to the dictionary table :return:
        """
        print("Adding " + bookpath + " to database")
        print("HERE1")
        self._add_pinyin_pages_to_book_table(bookpath)
        self._add_book_table_to_definitions_table(bookpath)

    def _save_yellowbridge_data(self, word, cache_number=None):
        '''
        Helper function for complete_unfinished_dictionary_records() Takes a word (one or more characters),
        finds them on yellowbridge, and adds them to the dictionary :param word: The word to find on yellowbridge.
        :param cache_number: The secondary page number for a word with multiple definitions. (See comments in body of
        function)
        :return:
        '''
        self.cursor.execute("SELECT word, definition FROM dictionary WHERE word = ?", [word])
        response = self.cursor.fetchall()
        if len(response) == 0:
            print(word + " is not in the database")
            return
        else:
            if response[0][1] is not None:
                # print("The definition for " + word + " is already in the dictionary")
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

            # Add the information for this word to the database
            self.cursor.execute("UPDATE dictionary "
                                "SET word_traditional = ?, "
                                "word_type = ?,"
                                "pinyin = ?, "
                                "pinyin_numbers = ?,"
                                "sub_components = ?,"
                                "hsk_level = ?,"
                                "top_level = ?,"
                                "definition = ?"
                                "WHERE word = ?",
                                [traditional_script, part_of_speech, pinyin, pinyin_num, composing_words, hsk_level,
                                 top_level,
                                 definition,
                                 word])
            self.connection.commit()
        else:
            # print("This is not a definition page. getting all sub-pages")
            matching_results = yellowbridge_soup.find(id='multiRow')
            # Grab first row. This is usually the most common definition
            row = matching_results.find_all('tr')[0]
            # print(row.find('a'))
            href = str(row.find('a')['href'])
            # print(href)
            cache_number_from_href = href.split("word=")[1].split("&")[1].replace("cache=", "")

            self._save_yellowbridge_data(word, cache_number_from_href)

    def complete_unfinished_dictionary_records(self):
        '''
        Scans through the database table called dictionary for rows that do not currently have a definition
        If one is found, it searches online for the definition.
        :return:
        '''
        print("Checking for records...")
        while True:
            self.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
            response_rows = self.cursor.fetchall()
            # print(response_rows)
            if len(response_rows) > 0:
                print("Adding " + str(len(response_rows)) + " rows to dictionary table")
                for row in response_rows:
                    word = row[0]
                    self._save_yellowbridge_data(word)
            else:
                print("No new rows to complete in dictionary table")
            time.sleep(2)

    def print_database_status(self):
        """
        Prints some basic information about the database
        :return:
        """
        self.cursor.execute("SELECT word FROM dictionary")
        all_rows = self.cursor.fetchall()
        self.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
        unfinished_rows = self.cursor.fetchall()
        format_string_int = "{:<30} | {:>8}"
        format_string_dec = "{:<30} | {:>8.2}"
        print("------------------------")
        print(self.database_name)
        print("------------------------")
        print(format_string_int.format("Number of books:", len(self.book_list)))
        print(format_string_dec.format("Database size (MB):", Path(self.database_name).stat().st_size / (1024 * 1024)))
        print("Dictionary Table:")
        print(format_string_int.format("Number of rows:", len(all_rows)))
        print(format_string_int.format("Number of unfinished rows:", len(unfinished_rows)))

    @property
    def book_list(self):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        return_array = []
        for table in cursor.fetchall():
            if table[0] != 'dictionary' and table[0] != 'sqlite_sequence':
                return_array.append(table[0])
        return return_array

    @book_list.setter
    def book_list(self, value):
        self._book_list = value
