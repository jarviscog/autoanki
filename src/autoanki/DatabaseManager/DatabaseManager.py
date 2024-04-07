import os
from string import punctuation
import re
import sqlite3
import logging
import unicodedata
from glob import glob

from pathlib import Path
import jieba
import chinese_converter

from autoanki.BookCleaner.BookCleaner import CLEANED_FILES_DIRECTORY

CHINESE_PUNC = "！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."
PUNC = "™∞•◎ "

class DatabaseManager:

    def __init__(self, database_path, debug_level):
        self.logger = logging.getLogger('autoanki.dbmngr')
        self.logger.setLevel(debug_level)
        if not os.path.exists(database_path):
            self.logger.warning("The database [", database_path, "] does not exist.")
            raise Exception("Cannot create DatabaseManager with invalid database path.")
        self.database_path = database_path
        self.books = []
        path = os.path.join(os.getcwd(), self.database_path)
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    @staticmethod
    def convert_to_tablename(name: str):
        """
        Converts a string to a sql-valid table name.
        `param name` The name to convert
        `return` A tablename valid for an sql table
        """
        value = unicodedata.normalize('NFKC', name)
        # value.replace("：",":")
        value = value.replace("：", "__")
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '_', value).strip('-_')

    @staticmethod
    def is_database(database_name:str):
        if not database_name.endswith(".db"):
            return False
        if not os.path.exists(database_name):
            return False
        try:
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            # This will fail if dictionary table does not exist
            cursor.execute("SELECT word FROM dictionary")
            connection.close()
        except sqlite3.OperationalError:
            return False
        return True

    @staticmethod
    def create_database(database_path):
        """
        Creates an autoanki database file, including all tables needed for autoanki
        `database_path` The path to the database to create
        """
        logger = logging.getLogger('autoanki.dbmngr')
        logger.info("Creating database [" + database_path + "]")
        path = os.path.join(os.path.dirname(__file__), 'databases_init.sql')
        try:
            with open(path, 'r') as sql_file:
                sql_script = sql_file.read()
            connection = sqlite3.connect(database_path)
            cursor = connection.cursor()
            cursor.executescript(sql_script)
            connection.commit()
        except FileNotFoundError:
            logger.warning("Could not create database: Missing SQL files")
            return False

    def _create_book_table(self, book_name, table_name) -> bool:
        """
        Creates a new entry in the book_list table
        `table_name` The name of the new entry to create
        `return` False if error
        """
        self.cursor.execute("SELECT table_name FROM book_list")
        book_list = self.cursor.fetchall()

        if (table_name,) in book_list:
            self.logger.warning("The book is already in database. Not adding")
            return False

        # self.logger.debug("Inserting")
        self.cursor.execute(f"INSERT INTO book_list VALUES(\"{book_name}\",\"{table_name}\",'cn')")
        self.connection.commit()
        fname = 'book_table.sql'
        this_file = os.path.abspath(__file__)
        this_dir = os.path.dirname(this_file)
        wanted_file = os.path.join(this_dir, fname)
        fd = open(wanted_file, 'r')
        book_table_file = fd.read()
        book_table_file = book_table_file.replace("BOOK_NAME", table_name)
        fd.close()
        # Create the new table
        self.cursor.execute(book_table_file)
        self.connection.commit()
        return True

    def add_file_to_database(self, filepath, table_name):
        """
        Adds every word in a file to both the dictionary table and the book's table
        `filepath` The path to the file
        `table_name` The name of the table to add the words to.
            This should be the same for every wile in a given book
        """
        self.logger.info(f"Adding file {filepath} to database...")


        word_appearances = {}
        with open(filepath,'r',encoding='utf-8') as f:
            line = " "
            while line:
                line = f.readline()
                if not line:
                    continue
                words = jieba.lcut(line)
                for word in words:

                    # Remove puncuation
                    word = word.translate(str.maketrans('', '', punctuation))

                    is_ascii = len(word) == len(word.encode())

                    is_ascii_special = False
                    if len(word) == 1:
                        is_ascii_special = ord(word[0]) > 128 and ord(word[0]) < 255 

                    if word in PUNC or word in CHINESE_PUNC or is_ascii or is_ascii_special or word is None:
                        continue
                    if word_appearances.get(word) == None:
                        # Convert the word to simplified if needed
                        word = chinese_converter.to_simplified(word)
                        word_appearances[word] = 1
                    else:
                        word_appearances[word] += 1



        # Add the words to the dictionary if they are not already there
        self.cursor.execute(f"SELECT word FROM dictionary")
        self.connection.commit()
        dictionary_words = self.cursor.fetchall()
        self.logger.info(f"{len(word_appearances.items())} words in file. {len(dictionary_words)} in dictionary.")

        for word, appearances in word_appearances.items():
            if (word,) not in dictionary_words:
                # self.logger.debug("Adding word...")
                self.cursor.execute(f"INSERT INTO dictionary (word) VALUES (?)", [word])
                self.connection.commit()

        # Make a dictionary of word ids from dictionary
        self.cursor.execute(f"SELECT word_id, word FROM dictionary")
        result = self.cursor.fetchall()
        word_id_dict = {}
        for line in result:
            word_id_dict[line[1]] = line[0]

        self.cursor.execute(f"SELECT dictionary_word_id, number_of_appearances FROM {table_name}")
        self.connection.commit()
        book_table_response = self.cursor.fetchall()
        book_table_appearances = {}
        # Get the number of appearances in the book table
        for i in book_table_response:
            book_table_appearances[i[0]] = i[1]
        # pprint.pprint(book_table_appearances)

        # Add all words to the book_table
        for word, appearances in word_appearances.items():

            dictionary_word_id = word_id_dict[word]

            # If the word is already in the dictionary, add the number of appearances to it
            if dictionary_word_id in book_table_appearances:
                file_appearances = word_appearances[word]
                db_appearances = book_table_appearances[dictionary_word_id]
                # print("File app:", file_appearances)
                # print("Book app:", book_table_appearances[dictionary_word_id])
                sum = file_appearances + db_appearances
                self.cursor.execute(f"UPDATE {table_name} SET number_of_appearances = ? "
                                    f"WHERE dictionary_word_id = ?", [sum, dictionary_word_id])
                self.connection.commit()

            else:
                self.cursor.execute(f"INSERT INTO {table_name} (dictionary_word_id, number_of_appearances) "
                                    f"VALUES (?,?)", [dictionary_word_id, word_appearances[word]])
                self.connection.commit()

        # self.logger.debug("Done adding file to database")

    def add_book(self, bookpath: str, book_name: str):
        """
        Adds a file to the autoanki database. This involves the following steps:\n
        1 - Add book to the book_list table
        2 - Add all the files in "bookpath" to the definitions table and book table
        3 - Add book to book_list property

        If given a directory, it will recursively search for all files in the directory and add them.

        if not already there, adding the
        :param bookpath: The filepath to the book. This is file, or a directory of files
        :param book_name: The name of the book. This will show up in the Anki deck
        :return: None
        """
        self.logger.info("Adding book...")

        # Gets a 'table name' clean version of the book name
        book_tablename = self.convert_to_tablename(book_name)

        # Add the name of the book to the book_list table
        success = self._create_book_table(book_name, book_tablename)
        if not success:
            self.logger.error("Failed to create book table")
            return

        self.logger.debug(bookpath)
        if os.path.isdir(bookpath):
            self.logger.debug("Directory found:")
            result = [y for x in os.walk(bookpath + '/' + CLEANED_FILES_DIRECTORY) for y in glob(os.path.join(x[0], '*.txt'))]
            for path in result:
                self.logger.debug(path)
                self.add_file_to_database(path, book_tablename)

        elif os.path.isfile(bookpath):
            self.logger.debug("File found:")
            # Add all the words in the book to the `definitions` table
            self.add_file_to_database(bookpath, book_tablename)

        else:
            self.logger.warning(f"Incorrect bookpath: [{bookpath}]")
            return False

        self.logger.info("Done adding book.")
        return True

    def print_info(self):
        """
        Print basic information about the database
        :return:
        """
        self.cursor.execute("SELECT word FROM dictionary")
        all_rows = self.cursor.fetchall()
        self.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
        unfinished_rows = self.cursor.fetchall()
        format_string_int = "{:<30} | {:>8}"
        format_string_dec = "{:<30} | {:>8.2}"
        print("------------------------")
        print(self.database_path)
        print("------------------------")
        print(format_string_int.format("Number of books:", len(self.books)))
        print(format_string_dec.format("Database size (MB):", Path(self.database_path).stat().st_size / (1024 * 1024)))
        print("Dictionary Table:")
        print(format_string_int.format("Number of rows:", len(all_rows)))
        print(format_string_int.format("Number of unfinished rows:", len(unfinished_rows)))

    def update_definition(self, params: list):
        f"""
        Complete a definition for one word in the dictionary table\n
        traditional_script = params[0]\n
        word_type = params[1]\n
        pinyin = params[2]\n
        pinyin_numbers = params[3]\n
        sub_components = params[4]\n
        hsk_level = params[5]\n
        top_level = params[6]\n
        definition = params[7]\n
        word = params[8]
        :param params: A list of params for the database:
        :return:
        """
        # TODO Some sanatization here might be a good idea
        #   Make sure junk data can't crash this function
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
                            params)
        self.connection.commit()

    def get_all_completed_definitions(self):

        self.cursor.execute("SELECT * FROM dictionary WHERE definition IS NOT NULL")
        raw_words = self.cursor.fetchall()

        # pprint.pp(raw_words)
        words = []
        for row in raw_words:
            word = {
                "word_id": row[0],
                "word": row[1],
                "word_traditional": row[2],
                "word_type": row[3],
                "pinyin": row[4],
                "pinyin_numbers": row[5],
                "number_of_strokes": row[6],
                "sub_components": row[7],
                "frequency": row[8],
                "hsk_level": row[9],
                "top_level": row[10],
                "audio_path": row[11],
                "image_path": row[12],
                "definition": row[13]
            }
            # print(word["word"])
            # pprint.pp(word)
            # words.append(word)
            words.append(word)
        # pprint.pp(words)
        return words

    def unfinished_definitions(self) -> int:
        self.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
        unfinished_rows = self.cursor.fetchall()
        return len(unfinished_rows)

    @property
    def books(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute("SELECT book_name FROM book_list")
        return_array = []
        for table in cursor.fetchall():
            return_array.append(table[0])
        return return_array

    @books.setter
    def books(self, value):
        self._books= value
