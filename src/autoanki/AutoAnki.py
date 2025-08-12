import logging
import pandas as pd
import pdfplumber
import os
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import importlib.metadata
import importlib.metadata
import time
import sys
from glob import glob
from pprint import pprint
from pprint import pformat

from autoanki.adapters import *
from autoanki.DeckManager import DeckManager


BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
RESET = "\u001b[0m"


def get_adapter(language_code: str, settings) -> LanguageAdapter | None:
    if language_code == "zh":
        return ChineseAdapter(settings)
    elif language_code == "fr":
        return FrenchAdapter(settings)
    return None


def get_folder_contents(directory: str) -> str:
    """Adds a book from a folder full of files
    Only opens any .txt files in the subdirectory
    """

    # Read all files into a string, and use to add from string
    all_files_contents = ""

    # self.logger.debug("Bookpath: " + directory)
    if os.path.isdir(directory):
        # self.logger.debug("Directory found:")
        text_files = [
            y for x in os.walk(directory) for y in glob(os.path.join(x[0], "*.txt"))
        ]
        for path in text_files:
            # self.logger.debug(path)
            # Open and append to string
            with open(path) as f:
                contents = f.read()
                all_files_contents += contents

    return all_files_contents


class AutoAnki:
    def __init__(
        self,
        language_code: str = "zh",
        debug_level=20,
        log_file=None,
        settings={},
    ):
        """
        Creates an instance of autoanki.
        This creates a database connection, dictionary connection, and deck maker
        Args:
            `language_code`: The language to load, as per its ISO 639-1 two-letter code (en, zh, fr...)
            `logging_level`: between 0 (DEBUG) and 50(CRITICAL)
            `log_file`: Location to store logs, otherwise will use stdout
            `settings`: Settings passed in for a given language. To see the options, check `autoanki/adapters/<language>`
        """
        self.logger = logging.getLogger("autoanki")

        self.logger.setLevel(debug_level)
        formatter = logging.Formatter(
            f"{GREEN}%(asctime)s{RESET} {RED}%(levelname)8s{RESET} {YELLOW}%(name)-16s{RESET}: %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        # logging.basicConfig(
        # #filename='HISTORY.log',
        # level=logging.WARNING,
        # format=f"{GREEN}%(asctime)s{RESET} {RED}%(levelname)8s{RESET} {YELLOW}%(name)-16s{RESET}: %(message)s",
        # datefmt="%Y-%m-%d %H:%M:%S",
        # )

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(debug_level)
        stdout_handler.setFormatter(formatter)
        self.logger.addHandler(stdout_handler)

        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(debug_level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        __version__ = importlib.metadata.version(__package__ or __name__)
        self.logger.info(f"===== {GREEN}autoanki version: {__version__} {RESET}=====")
        self.logger.info(
            f"===== {GREEN}Starting to load config: [{language_code}] {RESET}====="
        )

        total_start = time.time()
        self.language_adapter = get_adapter(language_code, settings)
        if not self.language_adapter:
            self.logger.error(f"Unsupported language: [{language_code}]")

        self.deck_manager = DeckManager(debug_level=debug_level)

        total_end = time.time()
        self.logger.info(
            f"===== {GREEN}Done init in {total_end - total_start:0.4f} seconds {RESET}====="
        )

    def add_book_from_string(self, contents: str, book_name: str = "unnamedbook"):
        """
        Add a book as a string to the database
        Args:
            `contents`: the contents of the book
            `book_name`: The name of the book being added e.g. "Lost Prince"
        """
        self.logger.debug(f"autoanki: Adding [{book_name}] from string")
        if not contents:
            self.logger.info(f"No contents supplied")
            return

        tokens = self.language_adapter.tokenize(contents)
        self.language_adapter.store(tokens, book_name)
        self.logger.info("autoanki: Added book from string.")

    def add_book_from_file(self, filepath: str, book_name: str = "unnamedbook"):
        """Add a file to the database
        Args:
            `filepath`: path to the directory that contains the files to add
            `book_name`: The name of the book being added e.g. "Lost Prince"
        """
        self.logger.debug(f"autoanki: Adding [{book_name}] from file: [{filepath}]")
        if not filepath:
            self.logger.info(f"No filepath supplied")
            return

        # Handle pdf
        extension = os.path.splitext(filepath)[1]

        # TODO handle PDFs
        #        if extension == ".pdf":
        #            self.logger.info(f"PDF detected")
        #            # for every page
        #            print(filepath)
        #            print(os.path.exists(filepath))
        #
        #            with pdfplumber.open(filepath) as pdf:
        #                print(pdf)
        #                for pages in pdf.pages:
        #                    print(pages.pages)
        #                    # print(pages.extract_text())
        #
        #                    text = pages.extract_text()
        #                    tokens = self.language_adapter.tokenize(text)
        #                    self.language_adapter.store(tokens)

        if extension == ".epub":
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

            tokens = self.language_adapter.tokenize(contents)
            self.language_adapter.store(tokens, book_name)

        elif extension == ".txt":
            self.logger.info(f"txt detected")
            # Add the book to the database
            if not os.path.isfile(filepath):
                self.logger.warning(f"File does not exist: [{filepath}]")
                return

            with open(filepath, "r") as file:
                contents = file.read()
            tokens = self.language_adapter.tokenize(contents)
            self.language_adapter.store(tokens, book_name)

        self.logger.info(f"autoanki: Added [{filepath}].")

    def add_book_from_folder(self, directory: str, book_name: str = "unnamedbook"):
        """
        Add a directory full of files to the database
        Args:
            `filepath`: path to the directory that contains the files to add
            `book_name`: The name of the book being added e.g. "Lost Prince"
        """
        # TODO this is broken
        self.logger.debug(
            f"autoanki: Adding [{book_name}] from directory: [{directory}]"
        )

        if not directory:
            self.logger.warning(f"No directory supplied")
            return

        # Add the book to the database
        contents = get_folder_contents(directory)
        tokens = self.language_adapter.tokenize(contents)
        self.language_adapter.store(tokens, book_name)
        self.logger.info(f"autoanki: Added [{directory}].")

    def add_book_from_pleco(self, filepath: str, book_name: str = "unnamedbook"):
        """Reads the contents of a Pleco export file (txt, not xml)
        Args:
            `filepath`: path to the directory that contains the files to add
            `book_name`: The name of the book being added e.g. "Lost Prince"
        """
        self.logger.debug(f"autoanki: Adding [{book_name}] from pleco: [{filepath}]")

        if not filepath:
            self.logger.warning(f"No filepath supplied")
            return

        with open(filepath, "r") as file:
            contents = file.read()
            for line in file.readlines():
                split_line = line.split(" ")
                if split_line:
                    contents += split_line[0]

        contents = ""
        self.logger.debug(f"Done reading Pleco. len: {len(contents)}")
        tokens = self.language_adapter.tokenize(contents)
        self.language_adapter.store(tokens, book_name)

    def pprint_unfinished_definitions(self):
        pprint(self.database_manager.unfinished_definitions())

    def get_number_of_words(self):
        return self.language_adapter.get_number_of_entries()

    def print_settings(self):
        self.logger.info("Settings:")
        for setting, value in self.language_adapter.get_settings().items():
            self.logger.info(f"{setting:<25} [{value}]")

    def create_deck(self, deck_name: str, filepath: str):
        """
        Creates a deck file in the directory of the main file.
        `deck_name` The name that will show up in Anki
        `filepath` Path to the file
        :return:
        """

        self.logger.info(f"Generating deck file [{deck_name}]")
        words = self.language_adapter.get_tokens_to_generate()
        deck_path = self.deck_manager.generate_deck_file(words, deck_name, filepath)
        if deck_path is None:
            self.logger.warning(f"Was not able to create deck file for [{deck_name}]")
        else:
            self.logger.info(f"Generated deck file [{deck_path}]")

    def save_dictionary_as_csv(self, filepath: str):
        # TODO this is broken
        self.logger.info("Saving to csv...")
        all = self.language_adapter.get_tokens_to_generate()

        df = pd.DataFrame(all)
        headers = self.language_adapter.get_note_fields("中文").keys()
        df.columns = headers
        df.to_csv(filepath)
        self.logger.info("Done saving to csv...")

    @property
    def book_list(self) -> list[str]:
        """
        Get a list of the books in the database
        :return: List of book names
        """
        return self.language_adapter.get_groups()

    @book_list.setter
    def book_list(self, _):
        pass

    @property
    def unfinished_entries(self):
        return self.database_manager.unfinished_definitions()

    @unfinished_entries.setter
    def unfinished_entries(self, _):
        pass
