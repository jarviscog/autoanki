import os
import pprint
import time
import sqlite3
import warnings
# import pprint
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pinyin as pin_to_num
from pathlib import Path
import unicodedata
import re


CLEANED_FILES_DIRECTORY = 'cleaned_files'


def convert_to_tablename(value):
    # TODO Look more into table name conventions (- vs. _ etc.)
    #   : in sql table name?
    #   Drop table??? Why is this not working
    value = str(value)
    value = unicodedata.normalize('NFKC', value)
    # value.replace("：",":")
    value = value.replace("：", "__")
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '_', value).strip('-_')


def is_database(database_name):
    try:
        if database_name.split(".")[1] != "db":
            return 0
        if not os.path.exists(database_name):
            return 0
        print("Got here")
        connection = sqlite3.connect(database_name)
        print("Got here")

        cursor = connection.cursor()
        # This will fail if dictionary table does not exist
        cursor.execute("SELECT word FROM dictionary")
    except:
        return 0
    return 1


# def is_valid_database_filename(filename : str):
#
#     filename = general_functions.slugify(filename)
#
#     if(filename.split('.')[-1] != 'db'):
#         return 0
#     return filename


def create_autoanki_db(database_path):

    # TODO: Make method not function
    print("DatabaseManager: Creating database [" + database_path + "]")
    path = os.path.join(os.path.dirname(__file__), 'databases_init.sql')
    with open(path, 'r') as sql_file:
        sql_script = sql_file.read()
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()

    # # Create book_table
    # path = os.path.join(os.path.dirname(__file__), 'databases_init.sql')
    # with open(path, 'r') as sql_file:
    #     sql_script = sql_file.read()
    # connection = sqlite3.connect(database_path)
    # cursor = connection.cursor()
    # cursor.executescript(sql_script)
    # connection.commit()


print("DatabaseManager: Done creating database!")


class DatabaseManager:

    def __init__(self, database_path):

        if not os.path.exists(database_path):
            warnings.warn("This database does not exist yet. Creating a new one...")
            create_autoanki_db(database_path)
        self.database_name = database_path
        self.book_list = []
        path = os.path.join(os.getcwd(), self.database_name)
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()


    def add_book(self, bookpath: str, book_name: str = "Unknown"):
        """
        Adds a file to the AutoAnki database. This involves:
        1 - Add book name to book_list table
        Find the sql friendly table name
        2 - Add all of the files in bookpath to the definitions table and book table
        3 - Add book to book_list property

        If given a directory, it will recursively search for all files in the directory and add them.

        if not already there, adding the
        :param bookpath: The filepath to the book. It is assumed this is a directory with the files to add
        :param book_name: The name of the book from which this
        :return: None
        """

        # Gets a 'table name' clean version of the book name
        table_book_name = convert_to_tablename(book_name)
        # print("Table book name: ", table_book_name)

        # Add the name of the book to the book_list table
        success = self._add_to_book_list_table(book_name, table_book_name)
        if not success:
            return

        # Add all the words in the bookpath to a new table with the name of the book. If a word is not in definitions,
        #   add it there first
        self.add_book_table_to_db(bookpath, table_book_name)
        if success is False:
            return

        return True

    def _add_to_book_list_table(self, book_name, table_name):
        """
        Creates a new entry in the book_list table
        :param table_name: The name of the new entry to create
        :return: False if error
        """
        # try:
        self.cursor.execute("SELECT table_name FROM book_list")
        list = self.cursor.fetchall()
        # print(list)

        # Check if the book is already there
        # If not, add the book to the table
        if (table_name,) not in list:
            # print("Inserting")
            self.cursor.execute(f"INSERT INTO book_list VALUES(\"{book_name}\",\"{table_name}\",'cn')")
            self.connection.commit()
        else:
            print("The book is already in database. Not adding")
            return False
        return True
        # except:
        #     return False

    def add_book_table_to_db(self, bookpath, table_name):
        """
        This is a bit complex, so I'll spell it out
        1. Index all the words contained in all the files in bookpath
        2. For each word:
            - Add to the dictionary table if not already there.
            - Add to the book table with the number of occurrences
        :param bookpath: The path to the
        :param table_name: The name of the table to create for the book
        :return:
        """
        # print("Making table...")
        # Collect list of all words in the book to put in the dictionary and book table
        files = []
        for r, d, f in os.walk(bookpath):
            for file in f:
                if '.txt' in file:
                    files.append(os.path.join(r, file))
        number_of_appearances = {}
        # print("Files to clean")
        # print(files)
        for filepath in files:
            with open(filepath,'r',encoding='utf-8') as f:
                line = " "
                i = 0
                while line:
                    line = f.readline()
                    i+=1
                    if line:
                        # TODO Use Language processing to get the words in the line.
                        for i in range(0,len(line)):
                            char = line[i]
                            if char != '\n':
                                print("Word: ",char)
                                if number_of_appearances.get(char) == None:
                                    number_of_appearances[char] = 1
                                else:
                                    number_of_appearances[char] += 1
                # pprint.pprint(number_of_appearances)

        # Add all words to the dictionary if they are not already there
        # I'm doing it this way to reduce the number of db calls, rather than checking if they are in the db one by one
        # Yes, this can create errors if 2 people are working on the same db, but this is sqlite
        self.cursor.execute(f"SELECT word FROM dictionary")
        dictionary_words = self.cursor.fetchall()

        for word, appearances in number_of_appearances.items():
            if (word,) not in dictionary_words:
                # print("Adding word...")
                self.cursor.execute(f"INSERT INTO dictionary (word) VALUES (?)", [word])
                self.connection.commit()

        # TODO Grab this from the SQL file rather than a string here
        # Create the new table
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}" (
                    book_table_word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dictionary_word_id INTEGER,
                    number_of_appearances INT,
                    FOREIGN KEY (dictionary_word_id) REFERENCES dictionary(word_id)
                )''')
        self.connection.commit()

        # Make a dictionary of word ids from dictionary
        self.cursor.execute(f"SELECT word_id, word FROM dictionary")
        result = self.cursor.fetchall()
        word_id_dict = {}
        for line in result:
            word_id_dict[line[1]] = line[0]

        # Add all words to the book_table
        for word, appearances in number_of_appearances.items():
            dictionary_word_id = word_id_dict[word]

            self.cursor.execute(f"INSERT INTO {table_name} (dictionary_word_id, number_of_appearances) "
                                f"VALUES (?,?)", [dictionary_word_id, number_of_appearances[word]])
            self.connection.commit()

        return True

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

    def _save_yellowbridge_data(self, word, cache_number=None):
        '''
        Helper function for complete_unfinished_dictionary_records() Takes a word (one or more characters),
        finds them on yellowbridge, and adds them to the dictionary
        :param word: The word to find on yellowbridge.
        :param cache_number: The secondary page number for a word with multiple definitions. (See comments in body of
        function)
        :return:
        '''
        print(repr(word))
        if word == None or word == '':
            print("There is no page on Yellowbridge page for null")
            return

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

    def get_book_definitions(self, book_name:str):
        self.cursor.execute(
            f"""
            Select 
                b.dictionary_word_id, 
                d.word, 
                d.word_traditional, 
                d.word_type, 
                d.pinyin, 
                d.pinyin_numbers, 
                d.hsk_level, 
                d.definition 
            FROM {book_name} b
            INNER JOIN dictionary d ON b.dictionary_word_id = d.word_id
            """
        )
        return self.cursor.fetchall()

    def complete_unfinished_definitions(self):
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
        cursor.execute("SELECT book_name FROM book_list")
        return_array = []
        for table in cursor.fetchall():
            return_array.append(table[0])
        return return_array

    @book_list.setter
    def book_list(self, value):
        self._book_list = value
