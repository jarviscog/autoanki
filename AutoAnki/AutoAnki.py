import os
import logging

from .BookCleaner import BookCleaner
from .DatabaseManager import DatabaseManager
from .DeckManager import DeckManager

__author__ = "Jarvis Coghlin"
__all__ = ['AutoAnki']
__version__ = "1.0.0"
__status__ = "Development"


class AutoAnki:

    def __init__(self, database_filepath='AutoAnki.db'):
        """
        Creates an instance of AutoAnki.
        This creates a book cleaner, database connection, and deck maker
        :param database_filepath: The filepath for the database
        """
        logging.info("AutoAnki: Connecting to database...")

        self.database_filepath = database_filepath

        self.book_cleaner = BookCleaner()
        self.database_manager = DatabaseManager(database_filepath)
        self.deck_manager = DeckManager(database_filepath)

        logging.info("AutoAnki: Connected!")

    def add_book(self, book_path: str, book_name: str = 'New Book'):
        """
        Add a directory ful of files to the database
        :param book_path: The filepath to the directory that contains the files to add. e.g. lost_prince.txt
        :param book_name: The name of the book being added e.g. "Lost Prince"
        :return:
        """

        logging.info("AutoAnki: Adding book...")

        # Clean the book
        if not self.book_cleaner.clean(book_path):
            logging.warning("AutoAnki: Unable to clean book [" + book_name + "].")
            return

        # Add the book to the database
        cleaned_path = os.path.join(book_path, "cleaned_files")
        if not self.database_manager.add_book(cleaned_path, book_name):
            logging.warning("AutoAnki: Unable to add [" + book_name + "] to database.")
            return

        logging.info("AutoAnki: Added [" + book_path + "].")

    def update_definitions(self):
        """
        AutoAnki contains an internal definitions' table that is scraped from the internet. As words are added to
        AutoAnki, their definitions must be found. This function passively finds definitions and adds them to the table
        :return: None
        """
        logging.info("AutoAnki: Updating definitions...")
        self.database_manager.complete_unfinished_definitions()

    def create_deck(self, deck_name:str):
        """
        Creates a deck file in the directory of the main file.
        FEATURE Add more options for how the deck looks
        :return:
        """

        logging.info("Generating deck file [" + deck_name + ".apk ]")
        deck_path = self.deck_manager.generate_deck_file(deck_name, self.database_filepath)
        if deck_path is None:
            logging.warning("Was not able to create deck file for [", deck_name, "]")
        else:
            logging.info("Generated deck file [" + deck_path + "]")

    @property
    def book_list(self):
        """
        Get a list of the books in the database
        :return: List of book names
        """
        return self.database_manager.book_list

    @book_list.setter
    def book_list(self, value):
        pass

    @property
    def unfinished_entries(self):
        return self.database_manager.unfinished_definitions()

    @unfinished_entries.setter
    def unfinished_entries(self, value):
        pass


if __name__ == '__main__':

    aa = AutoAnki()
    print(aa.book_list)
