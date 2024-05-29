import logging
import pandas as pd
import pdfplumber
import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from autoanki.BookCleaner import BookCleaner
from autoanki.DatabaseManager import ChineseDatabaseManager
from autoanki.DatabaseManager.DatabaseManager import DatabaseManager
from autoanki.Dictionary import CEDictionary
from autoanki.DeckManager import DeckManager
from autoanki.Dictionary.Dictionary import Dictionary
from autoanki.Tokenizer import ChineseTokenizer

import time

BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
RESET = "\u001b[0m"
logging.basicConfig(
    # filename='HISTORY.log',
    level=logging.WARNING,
    format=f"{GREEN}%(asctime)s{RESET} {RED}%(levelname)8s{RESET} {YELLOW}%(name)-16s{RESET}: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class LanguageResources:
    database_manager: DatabaseManager
    dictionary: Dictionary
    deck_manager: DeckManager


# class Chinese(LanguageResources):
# database_manager: ChineseDatabaseManager
# dictionary_manager: CEDictionary
# deck_manager: DeckManager

supported_languages = {"zh": "Yes"}


class AutoAnki:
    def __init__(
        self,
        language: str,
        database_filepath: str = "",
        debug_level=20,
        force=False,
        dictionary=None,
    ):
        """
        Creates an instance of autoanki.
        This creates a book cleaner, database connection, dictioary connection, and deck maker
        Args:
            `language`: The language to load, as per its ISO 639-1 two-letter code (en, zh, fr...)
            `database_filepath`: The filepath for the database. If none specified a new one will be created
            `logging_level`: between 0 (DEBUG) and 50(CRITICAL)
            `force`: Skip conformations for cleaning large numbers of files
        """
        self.logger = logging.getLogger("autoanki")
        self.logger.setLevel(debug_level)
        self.logger.debug(f"Autoanki logger active")

        if len(language) != 2:
            self.logger.warning(
                f"Incorrect language input: [{language}]. Please use it's 2-letter code"
            )
            return

        if not supported_languages.get(language):
            self.logger.warning(f"Unsupported language: [{language}]")
            return

        self.logger.info(
            f"===== {GREEN}Starting to load config: [{language}] {RESET}====="
        )
        total_start = time.time()
        self.force = force

        # self.book_cleaner = BookCleaner(debug_level, self.force)

        start = time.time()
        self.logger.info("Loading dictionary...")
        if dictionary:
            self.logger.info("Using custom dictionary")
            self.dictionary = dictionary
        else:
            self.dictionary = CEDictionary(debug_level)
        end = time.time()
        self.logger.info(f"Done in {end - start:0.4f} seconds")

        self.database_filepath = database_filepath
        if database_filepath == "":
            self.logger.info("No database specified. Creating a new one...")
            timestr = time.strftime("%Y%m%d_%H%M%S")
            self.database_filepath = str("autoanki_" + timestr + ".db")
            ChineseDatabaseManager.create_database(self.database_filepath)
        else:
            if not ChineseDatabaseManager.is_database(self.database_filepath):
                self.logger.info("Creating database...")
                ChineseDatabaseManager.create_database(self.database_filepath)
                self.logger.info("Done creating database.")

        start = time.time()
        self.logger.info("Connecting to database...")
        self.database_manager = ChineseDatabaseManager(
            self.database_filepath, debug_level, dictionary=self.dictionary
        )
        end = time.time()
        self.logger.info(f"Done in {end - start:0.4f} seconds")

        start = time.time()
        self.logger.info("Connecting to DeckManager...")
        self.deck_manager = DeckManager(debug_level)
        end = time.time()
        self.logger.info(f"Done in {end - start:0.4f} seconds")

        total_end = time.time()
        self.logger.info(
            f"===== {GREEN}Done loading profile in {total_end - total_start:0.4f} seconds {RESET}====="
        )

    def add_book_from_string(self, contents: str, book_name: str = "Book Name"):
        """
        Add a book as a string to the database
        Args:
            `contents`: the contents of the book
            `book_name`: The name of the book being added e.g. "Lost Prince"
        """
        self.logger.debug(f"autoanki: Adding book [{book_name}] from string")
        if not contents:
            self.logger.info(f"No contents supplied")
            return

        # TODO Handle pdfs in file
        # TODO Restructure so each file can be passed to database_manager and still get added to the same book

        # Add the book to the database
        if not self.database_manager.add_book_from_string(contents, book_name):
            self.logger.warning("Unable to add [" + book_name + "] to database.")
            return

        self.logger.info("autoanki: Added book from string.")

    def add_book_from_file(self, filepath: str, book_name: str = "Book Name"):
        """Add a file to the database
        Args:
            `filepath`: path to the directory that contains the files to add
            `book_name`: The name of the book being added e.g. "Lost Prince"
        """
        self.logger.debug(
            f"autoanki: Adding book [{book_name}] from file: [{filepath}]"
        )
        if not filepath:
            self.logger.info(f"No filepath supplied")
            return
        # pip3 install pdfplumber

        # Handle pdf
        extension = os.path.splitext(filepath)[1]

        if extension == ".pdf":
            self.logger.info(f"PDF detected")
            # for every page
            print(filepath)
            print(os.path.exists(filepath))

            with pdfplumber.open(filepath) as pdf:
                print(pdf)
                for pages in pdf.pages:
                    print(pages.pages)
                    print(pages.extract_text())
                    if not self.database_manager.add_book_from_string(
                        pages.extract_text(), book_name
                    ):
                        self.logger.warning(
                            "Unable to add [" + book_name + "] to database."
                        )
                        return
        elif extension == ".epub":
            book = epub.read_epub(filepath)
            # Get the chapters
            chapters = ""
            for html_element in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
                self.logger.info(html_element)
                chapters += str(html_element.get_content(), "utf-8")
            blacklist = [
                "[document]",
                "noscript",
                "header",
                "html",
                "meta",
                "head",
                "input",
                "script",
            ]
            # These come out as html, so convert to text
            contents = ""
            soup = BeautifulSoup(chapters, "html.parser")
            text = soup.get_text()

            text = soup.find_all(text=True)
            for t in text:
                if t.parent.name not in blacklist:
                    contents += "{} ".format(t)
            if not self.database_manager.add_book_from_string(contents, book_name):
                self.logger.warning("Unable to add [" + book_name + "] to database.")
                return
        elif extension == ".txt":
            self.logger.info(f"txt detected")
            # Add the book to the database
            if not self.database_manager.add_book_from_file(filepath, book_name):
                self.logger.warning("Unable to add [" + book_name + "] to database.")
                return

        self.logger.info("autoanki: Added [" + filepath + "].")

    def add_book_from_folder(self, directory: str, book_name: str = "Book Name"):
        """
        Add a directory full of files to the database
        Args:
            `filepath`: path to the directory that contains the files to add
            `book_name`: The name of the book being added e.g. "Lost Prince"
        """
        self.logger.debug(
            f"autoanki: Adding book [{book_name}] from directory: [{directory}]"
        )
        if not directory:
            self.logger.info(f"No directory supplied")
            return

        # Add the book to the database
        if not self.database_manager.add_book_from_folder(directory, book_name):
            self.logger.warning("Unable to add [" + book_name + "] to database.")
            return

        self.logger.info("autoanki: Added [" + directory + "].")

    def add_book_from_pleco(self, filepath: str, book_name: str):
        """Reads the contents of a Pleco export file (txt, not xml)
        Args:
            `filepath`: path to the directory that contains the files to add
            `book_name`: The name of the book being added e.g. "Lost Prince"
        """
        self.logger.debug(
            f"autoanki: Adding book [{book_name}] from pleco: [{filepath}]"
        )
        if not filepath:
            self.logger.info(f"No filepath supplied")
            return

        with open(filepath, "r") as file:
            contents = file.read()
            for line in file.readlines():
                split_line = line.split(" ")
                if split_line:
                    contents += split_line[0]

        contents = ""
        self.logger.debug(f"Done reading Pleco. len: {len(contents)}")
        self.database_manager.add_book_from_string(contents, book_name)

    def complete_unfinished_definitions(self):
        """
        autoanki contains an internal definitions table that is scraped from the internet. As words are added to
        autoanki, their definitions must be found.
        This function finds definitions and adds them to the table
        """
        start = time.time()
        self.logger.info("Checking for records...")
        response_rows = self.database_manager.unfinished_definitions()
        if len(response_rows) == 0:
            self.logger.info("No new rows to complete in dictionary table")
            return

        self.logger.info(
            "Adding " + str(len(response_rows)) + " rows to dictionary table"
        )
        self.tokenizer = ChineseTokenizer(dictionary=self.dictionary)
        for row in response_rows:
            word = str(row[0])

            # self.logger.debug(f"Finding: [{word}]")
            # self.logger.debug("Trying local dictionary...")
            params = self.dictionary.find_word(word)
            # self.logger.info(params)
            if params:
                # self.logger.debug(f"✅Found: [{params[8]}]")
                self.database_manager.update_definition(params)
                continue

            self.logger.info(f"❌Could not find: [{word}]")
        end = time.time()
        self.logger.info(
            f"Finished collecting definitions in {end - start:0.4f} seconds"
        )

    def deck_settings(
        self,
        include_traditional=True,
        include_part_of_speech=True,
        include_audio=False,
        include_pinyin=True,
        include_zhuyin=False,
        hsk_filter=None,
        word_frequency_filter=None,
    ):
        """Configures settings for what's in the deck, and how it looks"

        `word_frequency_filter`: Float between 0 and 1. 1 being every word is included, 0 being none are included
        """
        self.deck_manager.settings(
            include_traditional=include_traditional,
            include_pinyin=include_pinyin,
            include_zhuyin=include_zhuyin,
            include_part_of_speech=include_part_of_speech,
            include_audio=include_audio,
            word_frequency_filter=word_frequency_filter,
            hsk_filter=hsk_filter,
        )

    def print_database_info(self):
        self.database_manager.print_info()

    @staticmethod
    def is_database(db_path):
        return ChineseDatabaseManager.is_database(db_path)

    @staticmethod
    def create_database(db_path: str):
        ChineseDatabaseManager.create_database(db_path)

    def create_deck(self, deck_name: str, filepath: str):
        """
        Creates a deck file in the directory of the main file.
        `deck_name` The name that will show up in Anki
        `filepath` Path to the file
        :return:
        """

        self.logger.info("Generating deck file [" + deck_name + ".apk]")
        words = self.database_manager.get_all_completed_definitions()

        deck_path = self.deck_manager.generate_deck_file(words, deck_name, filepath)
        if deck_path is None:
            self.logger.warning(
                "Was not able to create deck file for [", deck_name, "]"
            )
        else:
            self.logger.info("Generated deck file [" + deck_path + "]")

    def save_dictionary_as_csv(self, filepath: str):
        self.logger.info("Saving to csv...")
        all = self.database_manager.get_all_definitions()
        # pprint(all)

        df = pd.DataFrame(all)
        headers = self.database_manager.get_columns()
        df.columns = headers
        df.to_csv(filepath)
        self.logger.info("Done saving to csv...")

    @property
    def book_list(self):
        """
        Get a list of the books in the database
        :return: List of book names
        """
        return self.database_manager.books

    @book_list.setter
    def book_list(self, _):
        pass

    @property
    def unfinished_entries(self):
        return self.database_manager.unfinished_definitions()

    @unfinished_entries.setter
    def unfinished_entries(self, _):
        pass
