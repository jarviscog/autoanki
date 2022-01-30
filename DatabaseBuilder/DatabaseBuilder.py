import math

import general_functions
import os
from os.path import isfile, join
from selenium import webdriver
import time
import sqlite3

GARBAGE_SENTENCES = {
    "\n",
    "",
    "。"
}


def clean_page(page_path):
    """
    Takes a txt file and cleans it up, putting every sentence on a new line
    :param page_path: The txt file to clean
    :return:
    """

    # Clean page file of characters that may cause issues, and create example_clean.txt
    split_page_path = general_functions.split_filename(page_path)
    page_file = open(page_path, encoding='utf-8')
    page_string = ""

    for i in range(general_functions.file_len(page_path)):
        page_string += page_file.readline().strip("\n").strip("·")

    page_sentences = page_string.split("。")
    cleaned_file = open(split_page_path[0] + "_clean.txt", "w", encoding='utf-8')

    for page_sentence in page_sentences:
        page_sentence = page_sentence.lstrip().rstrip()
        if page_sentence not in GARBAGE_SENTENCES:
            cleaned_file.write(page_sentence + "。" + "\n")


class DatabaseBuilder:
    directory = ""
    compacted_pages_directory = directory + "\\" + "compacted_pages"
    pinyin_pages_directory = directory + "\\" + "pinyin_pages"
    pages = []
    database_name = "AutoAnki.db"
    database_table_name = ""

    # In bytes. One utf-8 character is 3 bytes. One ASCII character is 1 byte
    # This could be a more exact number (1024b not 1000b), but better to be on the low end then the website refuse.
    MAX_TXT_TO_PINYIN_SIZE = 270000

    # directory - the directory with the pages to add to the database
    def __init__(self, directory):

        self.directory = directory
        self.init_variables()

    def init_variables(self):

        self.compacted_pages_directory = self.directory + "\\" + "compacted_pages"
        self.pinyin_pages_directory = self.directory + "\\" + "pinyin_pages"
        self.pages = [f for f in os.listdir(self.directory) if (isfile(join(self.directory, f)) and f.endswith(".txt"))]
        self.database_table_name = self.directory.split("\\")[-1]
        print(self.database_table_name)
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.database_table_name} (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                word VARCHAR(255) NOT NULL UNIQUE,
                number_of_appearances INT
            )''')

    def clean_pages(self):

        for page in self.pages:
            clean_page(self.directory + page)

    def compact_pages(self):
        """
        Compacts all of the different pages in this directory into a specified size.
        Compacted in this context means that the files are re-organized by size, not chapter/webpage
        Some websites used have a free limit of 300kb, for example. Rather then pass all of these pages through one by
        one, it is more efficient to compact these into 299kb files and send those.
        :return: True if successful

        """
        print("Compacting files in " + self.directory + "...")
        try:
            os.mkdir(self.directory + "\\" + "compacted_pages")
        except FileExistsError:
            pass
        # This is all of the lines from all text files in the directory
        all_pages_text = ""

        for page_path in self.pages:
            page = open(self.directory + "\\" + page_path, "r", encoding="utf-8")
            for i in range(general_functions.file_len(self.directory + "\\" + page_path)):
                all_pages_text += page.readline()

        print("Found " + str(len(self.pages)) + " pages totalling " + str(len(all_pages_text)))

        # Splits the all_pages_text into smaller parts and saves it to the compacted_pages directory
        i, current_compacted_filename_number = 0, 0
        all_pages_sentances = all_pages_text.split("\n")
        current_compacted_file_size = 0
        current_compacted_file_text = ""
        while i < len(all_pages_sentances):

            current_sentance = all_pages_sentances[i]

            # If the current file has hit its limit, start a new compacted file and reset all variables
            if (len(current_sentance) + current_compacted_file_size) > self.MAX_TXT_TO_PINYIN_SIZE:
                current_compacted_filename_number += 1
                current_file = open(self.compacted_pages_directory + "\\" + "compacted-" + str(
                    current_compacted_filename_number) + ".txt", "w",
                                    encoding="utf-8")
                for line in current_compacted_file_text.split("\n"):
                    current_file.write(line + "\n")
                current_file.close()
                current_compacted_file_size = 0
                current_compacted_file_text = ""

            # Chinese characters are utf-8, meaning they are 8 bytes
            current_compacted_file_size += len(current_sentance) * 3
            current_compacted_file_text += current_sentance
            # A newline character is one byte
            current_compacted_file_size += 1
            current_compacted_file_text += "\n"

            i += 1

        current_compacted_filename_number += 1
        current_file = open(
            self.compacted_pages_directory + "\\" + "compacted-" + str(current_compacted_filename_number) + ".txt", "w",
            encoding="utf-8")
        for line in current_compacted_file_text.split("\n"):
            current_file.write(line + "\n")
        current_file.close()

        print("Done compacting")
        return True

    def get_pinyin_of_pages(self, headless=True):
        print("Getting pinyin")
        try:
            os.mkdir(self.pinyin_pages_directory)
            print("Created ")
        except FileExistsError:
            pass

        filenames_to_convert = [f for f in os.listdir(self.compacted_pages_directory) if
                                isfile(join(self.compacted_pages_directory, f))]
        for filename_to_convert in filenames_to_convert:
            if os.path.exists(self.pinyin_pages_directory + "\\" + filename_to_convert):
                print('getPinyin() already done')
            else:

                chrome_options = webdriver.ChromeOptions()
                chrome_options.headless = headless
                path = os.path.dirname(os.path.abspath(__file__))
                prefs = {"download.default_directory": path + "\\" + self.pinyin_pages_directory}
                # print("Download path: " + path + "\\" + self.pinyin_pages_directory)
                chrome_options.add_experimental_option("prefs", prefs)
                url = 'https://www.purpleculture.net/chinese-pinyin-converter/'
                driver = webdriver.Chrome(chrome_options=chrome_options,
                                          executable_path=str(os.getcwd() + "\\" + 'chromedriver.exe'))
                driver.get(url)
                # Grabs the definition part of the screen
                file_tab = driver.find_element_by_xpath('//*[@id="columnCenter"]/div[4]/div[1]/ul/li[2]/a')
                file_tab.click()
                upload_box = driver.find_element_by_id('txtfile')
                upload_box.send_keys(os.getcwd() + "\\" + self.compacted_pages_directory + "\\"
                                     + filename_to_convert)
                convert_button = driver.find_element_by_xpath('//*[@id="fileuploadform"]/div[2]/div/button[1]')
                convert_button.click()
                # Wait until file is in downloads file. Times out after 15 seconds
                for i in range(30):
                    if os.path.exists(self.pinyin_pages_directory + "\\" + filename_to_convert):
                        break
                    time.sleep(0.5)
                    if i == 29:
                        print("getPinyin File not downloaded correctly")
                driver.quit()

    def add_pinyin_pages_to_book_table(self):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        print("Adding pinyin pages to database...")
        filenames_to_add = [f for f in os.listdir(self.pinyin_pages_directory) if
                            isfile(join(self.pinyin_pages_directory, f))]

        number_of_words_added, number_of_words_not_added = 0, 0
        number_of_appearances_dict = {}

        for filename_to_add in filenames_to_add:

            valid_entries, invalid_rows = {}, {}
            valid_rows_num, invalid_rows_num = 0, 0

            file_to_add_length = general_functions.file_len(self.pinyin_pages_directory + "\\" + filename_to_add)
            page = open(self.pinyin_pages_directory + "\\" + filename_to_add, "r", encoding="utf-8")
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

        # Take the number_of_appearances_dict dict and add all items to the database
        # print("Number of words in number_of_appearances_dict: " + str(len(number_of_appearances_dict)))
        for word, appearances in number_of_appearances_dict.items():
            if word not in GARBAGE_SENTENCES:
                cursor.execute(f"SELECT * FROM {self.database_table_name} WHERE word = ?", [word])
                response = cursor.fetchall()
                if len(response) > 0:
                    # print("Word " + word + " is already in db")
                    response_word_id, response_word, response_word_appearances = response[0]
                    combined_appearances = appearances + response_word_appearances
                    cursor.execute(f"UPDATE {self.database_table_name} SET number_of_appearances = ? WHERE word = ?",
                                   [combined_appearances, word])
                    connection.commit()
                else:
                    cursor.execute(
                        f"INSERT INTO {self.database_table_name} (word, number_of_appearances) VALUES (?, ?)",
                        [word, appearances])
                    connection.commit()

                # for row in cursor.fetchall():
                #     print("CURSOR ROW: ")
                #     print(row)
                #     time.sleep(1)

        print("---Done adding new table to database!---")
        print("---Words added: " + str(number_of_words_added) + "---")
        print("---Words not added: " + str(number_of_words_not_added) + "---")
        # TODO Fix the terrible book coverage from parsing sentences in chapter files (about 10% right now)
        print("---Book coverage: " + "{0:.2f}".format(
            (number_of_words_added / (number_of_words_added + number_of_words_not_added)) * 100)
              + "%---")
        connection.close()

    def add_book_table_to_definitions_table(self):
        """
        Takes all rows from the book table and adds them to the definitions table if they are not there already
        :return:
        """
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {self.database_table_name} WHERE word IS NOT NULL")
        book_table_rows = cursor.fetchall()
        for book_table_row in book_table_rows:
            book_table_id, book_table_word, book_table_number_of_appearances = book_table_row
            print("Current row: " + str(book_table_id) + " " + str(book_table_word) + " " + str(book_table_number_of_appearances))
            # print("Response length: " + str(len(response)))
            cursor.execute("SELECT * FROM dictionary WHERE word = ?", [book_table_word])
            response = cursor.fetchall()

            if len(response) > 0:
                print("Entry already present")
                # print(response)
            else:
                print("Entry not present. Adding...")
                cursor.execute(f"INSERT INTO dictionary (word) VALUES (?)", [book_table_word])
                connection.commit()

    def add_to_database(self):

        print("Adding to database...")

        # self.clean_pages()
        self.compact_pages()
        self.get_pinyin_of_pages(headless=False)
        self.add_pinyin_pages_to_book_table()
        self.add_book_table_to_definitions_table()
