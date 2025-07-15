import os
import sqlite3
import logging
from glob import glob
import time
import operator
from pprint import pprint

from pathlib import Path
from collections import Counter

from autoanki.database import DatabaseManager
from autoanki.tokenizer import ChineseTokenizer

BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
RESET = "\u001b[0m"

DICT_ENTRY = {
    "number_of_occurrences": 0,
    "word": "",
    "word_traditional": "",
    "pinyin": "",
    "pinyin_numbers": "",
    "zhuyin": "",
    "jyutping": "",
    "part_of_speech": "",
    "number_of_strokes": 0,
    "sub_components": "",
    "definition": "",
    "frequency": 0,
    "hsk_level": 0,
    "tocfl_level": 0,
    "audio_path": "",
    "image_path": "",
    "character_graphic": "",
    "examples": [],
}


def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination


class ChineseDatabaseManager(DatabaseManager):
    def __init__(self, debug_level, dictionary=None):
        """Contains all entries, including number of occurrences, word, and definition"""
        self.logger = logging.getLogger("autoanki.dbmngr")
        self.logger.setLevel(debug_level)

        self.database = {}
        self.book_list = []

        # Text segmenter
        self.tokenizer = ChineseTokenizer(debug_level, dictionary=dictionary)

        self.books = []

    def add_contents_to_database(self, contents: str):
        """Adds every word in a file to both the dictionary table and the book's table
        Args:
            `contents`:
        """
        self.logger.info(f"Adding contents to database...")
        word_appearances = {}
        # lines = contents.splitlines()
        self.logger.debug(f"Tokenizing...")
        start = time.time()
        tokens = self.tokenizer.tokenize(contents)
        end = time.time()
        if not tokens:
            self.logger.error(f"No tokens returned")
            return
        self.logger.info(
            f"Tokenized in {GREEN}{end - start:0.4f}{RESET} seconds. Tokens: [{len(tokens)}]"
        )
        if not tokens:
            return

        self.logger.debug(f"Generating dict...")
        start = time.time()

        for token in tokens:
            if not token:
                continue
            if word_appearances.get(token) == None:
                word_appearances[token] = 1
            else:
                word_appearances[token] += 1

        new_dict = {}
        for key, number_of_appearances in word_appearances.items():
            entry = DICT_ENTRY.copy()
            entry["number_of_appearances"] = number_of_appearances
            new_dict[key] = entry

        end = time.time()
        self.logger.info(f"Generated dict in {GREEN}{end - start:0.4f}{RESET} seconds")

        self.logger.debug(f"Merging into existing dict...")
        start = time.time()

        self.database = merge(self.database, new_dict)

        end = time.time()
        self.logger.info(
            f"Merged in {GREEN}{end - start:0.4f}{RESET} seconds. Total dict entries: [{len(self.database)}]"
        )

    def insert_word(self, word):
        # TODO Doing this breaks the `number_of_appearances`. This is a temporary fix
        # TODO This is really ineficcient
        #   Either contain an internal dict of words in the dictionary,
        #   or wrap this with a try catch
        if word in self.database:
            self.logger.warning(f"Word: [{word}] already in dict. Not adding")
            return
        entry = DICT_ENTRY.copy()
        entry["number_of_appearances"] = 1
        self.database[word] = entry

    def remove_word(self, word: str):
        # TODO: Make more stringent constraints on removing words. This should be extremely rare
        if word not in self.database:
            self.logger.warning(f"Word: [{word}] not in dict. Not deleting")
        del self.database[word]

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
        # TODO: This looks like it only reads txt files. Make sure this also works for other formats
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
        Args:
            `bookpath`: The filepath to the book. This is file, or a directory of files
            `book_name: The name of the book. This will show up in the Anki deck
        """
        # self.logger.info("Adding book...")
        # Add the name of the book to the book_list table
        if book_name not in self.book_list:
            self.book_list.append(book_name)

        # Add all the words in the book to the `definitions` table
        self.add_contents_to_database(contents)

        self.logger.debug("Done adding book.")
        return True

    def get_columns(self) -> list[str]:
        return list(DICT_ENTRY.keys())

    def get_length(self) -> int:
        return len(self.database)

    def update_definition(self, word, params: dict):
        try:
            self.database[word] = params
        except KeyError:
            self.logger.error(f"Error with: [{word}]")
            self.logger.error(params)
        return

    def get_all_definitions(self) -> dict:
        return self.database

    def get_all_completed_definitions(self) -> dict[str, dict]:
        # for key, value in self.database.items():
        # if "definition" not in value.keys():
        # TODO: Fix
        # self.logger.error(f"Broken keys: [{key}]")
        # self.logger.error(f"{value}")
        filtered_dict = {
            k: v
            for (k, v) in self.database.items()
            if ("definition" in v and v["definition"] != "")
        }
        return filtered_dict

    def unfinished_definitions(self):
        filtered_dict = {
            k: v for (k, v) in self.database.items() if (v["definition"] == "")
        }
        return filtered_dict

    @property
    def books(self) -> list[str]:
        return self.book_list

    @books.setter
    def books(self, value):
        self._books = value
