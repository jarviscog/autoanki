import os
import sqlite3
import logging
from glob import glob

from pathlib import Path

from autoanki.Tokenizer.ChineseTokenizer import ChineseTokenizer
from autoanki.DatabaseManager.DatabaseManager import DatabaseManager


class ChineseDatabaseManager(DatabaseManager):
    def __init__(self, database_path, debug_level, dictionary=None):
        """Interfaces with an SQLLite database containing information on words, definitions, and more"""
        self.logger = logging.getLogger("autoanki.dbmngr")
        self.logger.setLevel(debug_level)

        # Init database
        if not os.path.exists(database_path):
            self.logger.warning("The database [", database_path, "] does not exist.")
            raise Exception("Cannot create DatabaseManager with invalid database path.")
        self.database_path = database_path

        # Text segmenter
        self.tokenizer = ChineseTokenizer(debug_level, dictionary=dictionary)

        # Sql connection
        path = os.path.join(os.getcwd(), self.database_path)
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

        self.books = []

    @staticmethod
    def create_database(database_path: str):
        """Creates autoanki database file, including all tables needed
        Args:
            `database_path`: The path to the database to create
        """
        logger = logging.getLogger("autoanki.dbmngr")
        logger.info("Creating database [" + database_path + "]")
        path = os.path.join(os.path.dirname(__file__), "databases_init.sql")
        try:
            with open(path, "r") as sql_file:
                sql_script = sql_file.read()
            connection = sqlite3.connect(database_path)
            cursor = connection.cursor()
            cursor.executescript(sql_script)
            connection.commit()
            return True
        except FileNotFoundError:
            logger.warning("Could not create database: Missing SQL files")
            return False

    def _create_book_table(self, book_name, table_name) -> bool:
        """Creates a new entry in the book_list table
        Args:
            `table_name`: The name of the new entry to create
        Return:
            False if error
        """
        self.cursor.execute("SELECT table_name FROM book_list")
        book_list = self.cursor.fetchall()

        if (table_name,) in book_list:
            self.logger.warning("The book is already in database. Not adding")
            return False

        # self.logger.debug("Inserting")
        self.cursor.execute(
            f'INSERT INTO book_list VALUES("{book_name}","{table_name}",\'cn\')'
        )
        self.connection.commit()
        fname = "book_table.sql"
        this_file = os.path.abspath(__file__)
        this_dir = os.path.dirname(this_file)
        wanted_file = os.path.join(this_dir, fname)
        fd = open(wanted_file, "r")
        book_table_file = fd.read()
        book_table_file = book_table_file.replace("BOOK_NAME", table_name)
        fd.close()
        # Create the new table
        self.cursor.execute(book_table_file)
        self.connection.commit()
        return True

    def add_contents_to_database(self, contents: str, table_name: str):
        """Adds every word in a file to both the dictionary table and the book's table
        Args:
            `filepath`: The path to the file
            `table_name`: The name of the table to add the words to.
                This should be the same for every wile in a given book
        """
        self.logger.info(f"Adding contents to database...")
        word_appearances = {}
        lines = contents.splitlines()
        for line in lines:
            if not line:
                continue
            words = self.tokenizer.tokenize(line)
            if not words:
                continue
            for word in words:
                if word_appearances.get(word) == None:
                    word_appearances[word] = 1
                else:
                    word_appearances[word] += 1

        # Add the words to the dictionary if they are not already there
        self.cursor.execute(f"SELECT word FROM dictionary")
        self.connection.commit()
        dictionary_words = self.cursor.fetchall()
        self.logger.info(
            f"{len(word_appearances.items())} words in file. {len(dictionary_words)} in dictionary."
        )

        for word, appearances in word_appearances.items():
            if (word,) not in dictionary_words:
                self.insert_word(word)

        # Make a dictionary of word ids from dictionary
        self.cursor.execute(f"SELECT word_id, word FROM dictionary")
        result = self.cursor.fetchall()
        word_id_dict = {}
        for line in result:
            word_id_dict[line[1]] = line[0]

        self.cursor.execute(
            f"SELECT dictionary_word_id, number_of_appearances FROM {table_name}"
        )
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
                self.cursor.execute(
                    f"UPDATE {table_name} SET number_of_appearances = ? "
                    f"WHERE dictionary_word_id = ?",
                    [sum, dictionary_word_id],
                )
                self.connection.commit()

            else:
                self.cursor.execute(
                    f"INSERT INTO {table_name} (dictionary_word_id, number_of_appearances) "
                    f"VALUES (?,?)",
                    [dictionary_word_id, word_appearances[word]],
                )
                self.connection.commit()

        # self.logger.debug("Done adding file to database")

    def insert_word(self, word):
        # TODO Doing this breaks the `number_of_appearances`. This is a temporary fix
        # TODO This is really ineficcient
        #   Either contain an internal dict of words in the dictionary,
        #   or wrap this with a try catch
        self.cursor.execute("SELECT word FROM dictionary WHERE word = ?", [word])
        all_rows = self.cursor.fetchall()
        if len(all_rows) == 0:
            # self.logger.info("  Inserting")
            self.cursor.execute(f"INSERT INTO dictionary (word) VALUES (?)", [word])
            self.connection.commit()

    def remove_word(self, word: str):
        # TODO: Make more stringent constraints on removing words. This should be extremely rare
        if len(word) > 10:
            self.logger.warning(f"Not executing: [{word}]. Suspiciously large")
            return
        if "*" in word:
            self.logger.warning(f"Not executing: [{word}]. Star in command")
            return
        self.cursor.execute(f"DELETE FROM dictionary WHERE word=(?)", [word])
        self.connection.commit()

    def add_book_from_string(self, contents: str, book_name: str) -> bool:
        return self._add_book(contents, book_name)

    def add_book_from_file(self, filepath: str, book_name: str) -> bool:
        if not os.path.isfile(filepath):
            self.logger.info(f"File does not exist: [{filepath}]")
            return False

        with open(filepath, "r") as file:
            contents = file.read()
            return self._add_book(contents, book_name)

    def add_book_from_folder(self, directory: str, book_name: str) -> bool:
        """Adds a book from a folder full of files
        Only opens any .txt files in the subdirectory
        """
        self.logger.info(f"Adding folder [{directory}] to database")

        # Read all files into a string, and use to add from string
        all_files_contents = ""

        self.logger.debug("Bookpath: " + directory)
        if os.path.isdir(directory):
            self.logger.debug("Directory found:")
            text_files = [
                y for x in os.walk(directory) for y in glob(os.path.join(x[0], "*.txt"))
            ]
            for path in text_files:
                self.logger.debug(path)
                # Open and append to string
                with open(path) as f:
                    contents = f.read()
                    all_files_contents += contents

        self.add_book_from_string(all_files_contents, book_name)
        return True

    def _add_book(self, contents: str, book_name: str) -> bool:
        """Adds a file to the autoanki database.
        This involves the following steps:\n
        1 - Add book to the `book_list` table
        2 - Add all the files in "bookpath" to the definitions table and book table
        Args:
            `bookpath`: The filepath to the book. This is file, or a directory of files
            `book_name: The name of the book. This will show up in the Anki deck
        """
        self.logger.info("Adding book...")
        # Get a 'table name' clean version of the book name
        book_tablename = self.convert_to_tablename(book_name)
        # Add the name of the book to the book_list table
        success = self._create_book_table(book_name, book_tablename)
        if not success:
            self.logger.error(f"Failed to create book table: [{book_tablename}]")
            return False

        # Add all the words in the book to the `definitions` table
        self.add_contents_to_database(contents, book_tablename)

        self.logger.info("Done adding book.")
        return True

    def get_columns(self) -> list:

        return [
            "word_id",
            "word",
            "word_traditional",
            "pinyin",
            "pinyin_numbers",
            "zhuyin",
            "jyutping",
            "part_of_speech",
            "number_of_strokes",
            "sub_components",
            "definition",
            "frequency",
            "hsk_level",
            "tocfl_level",
            "audio_path",
            "image_path",
            "character_graphic",
            "examples",
        ]

    def print_info(self):
        """Print basic information about the database"""
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
        print(
            format_string_dec.format(
                "Database size (MB):",
                Path(self.database_path).stat().st_size / (1024 * 1024),
            )
        )
        print("Dictionary Table:")
        print(format_string_int.format("Number of rows:", len(all_rows)))
        print(
            format_string_int.format("Number of unfinished rows:", len(unfinished_rows))
        )

    def update_definition(self, params: dict[str, str]):
        """ """
        f"""Complete a definition for one word in the dictionary table\n
		Here is all of the fields that a card could have:
			word
			word traditional 
			pinyin
			pinyin numbers
			zhuyin
			jyutping
			part of speech
			number of strokes
			sub components
			definition
			frequency
			HSK level
			tocfl level
			audio path
			image path
			stroke order graphic
			examples
        :param params: A list of params for the database:
        :return:
        """

        try:
            self.cursor.execute(
                "UPDATE dictionary SET "
                "word_traditional = ?,"
                "pinyin = ?,"
                "pinyin_numbers = ?,"
                "zhuyin = ?,"
                "jyutping = ?,"
                "part_of_speech = ?,"
                "number_of_strokes = ?,"
                "sub_components = ?,"
                "definition = ?,"
                "frequency = ?,"
                "HSK_level = ?,"
                "tocfl_level = ?,"
                "audio_path = ?,"
                "image_path = ?,"
                "character_graphic= ?,"
                "examples = ?"
                "WHERE word = ?",
                [
                    params.get("word_traditional"),
                    params.get("pinyin"),
                    params.get("pinyin_numbers"),
                    params.get("zhuyin"),
                    params.get("jyutping"),
                    params.get("part_of_speech"),
                    params.get("number_of_strokes"),
                    params.get("sub_components"),
                    params.get("definition"),
                    params.get("frequency"),
                    params.get("HSK_level"),
                    params.get("tocfl_level"),
                    params.get("audio_path"),
                    params.get("image_path"),
                    params.get("character_graphic"),
                    params.get("examples"),
                    params.get("word"),
                ],
            )
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error updating database definition. Params:\n {params}")
            self.logger.error(f"Error: {e}")

    def get_all_definitions(self):
        self.cursor.execute("SELECT * FROM dictionary")
        words = self.cursor.fetchall()
        return words

    def get_all_completed_definitions(self):
        self.cursor.execute("SELECT * FROM dictionary WHERE definition IS NOT NULL")
        words = self.cursor.fetchall()
        return words

    def unfinished_definitions(self, column: str = "definition"):
        self.cursor.execute(f"SELECT word FROM dictionary WHERE {column} IS NULL")
        unfinished_rows = self.cursor.fetchall()
        return unfinished_rows

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
        self._books = value
