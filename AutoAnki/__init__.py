from .DatabaseManager import DatabaseManager
from .BookCleaner import BookCleaner
# from .DeckManager import DeckManager
import os
# import warnings



__author__ = "Jarvis Coghlin 2022"

__all__ = ['AutoAnki']



"""
inputs
database filepath (optional)

functions
- add book (with book title)
- collect definitions
- create deck file from list of books

properties 
- file_list
- unfinished_entries

"""

# TODO Learn the logging library to stop using print statements


class AutoAnki:

    def __init__(self, database_filepath='AutoAnki.db'):
        """
        The main AutoAnki object
        :param database_filepath:
        """
        # print("AutoAnki: Connecting to database...")
        self.book_cleaner = BookCleaner()
        self.database_filepath = database_filepath
        self.database_manager = DatabaseManager(database_filepath)
        self.database_manager
        # self.deck_manager = DeckManager(path)
        # print("AutoAnki: Connected!")

    def add_book(self, path: str, book_name: str = 'Unnamed', notify=False):
        """
        Add a directory ful of files to the database
        :param path: The filepath to the directory that contains the files to add
        :param book_name: The name of the book being added
        :return:
        """
        # print("\nAutoAnki: Adding book...")

        # Clean the book
        success = self.book_cleaner.clean(path)
        if success is False:
            return

        # Add the book to the database
        cleaned_path = os.path.join(path, "cleaned_files")
        success = self.database_manager.add_book(cleaned_path, book_name)
        if not success:
            # TODO Make this an error, not a print statement
            print("AutoAnki: Was unable to add [" + book_name + "].")
            return
        if notify:
            print("AutoAnki: Added [" + path + "].")

    def update_definitions(self):
        """
        AutoAnki contains an internal definitions' table that is scraped from the internet. As words are added to
        AutoAnki, their definitions must be found. This function passively finds definitions and adds them to the table
        :return: None
        """
        print("AutoAnki: Updating definitions...")
        # TODO Do some unit testing on this
        self.database_manager.complete_unfinished_definitions()

    @property
    def book_list(self):
        """
        Get a list of the books in the database
        :return: list of book names (str)
        """

        return self.database_manager.book_list

    @book_list.setter
    def book_list(self, value):
        self.book_list = value

    @property
    def unfinished_entries(self):
        # TODO Get num of unfinished entries
        return 0

    @unfinished_entries.setter
    def unfinished_entries(self, value):

        self.unfinished_entries = value


if __name__ == '__main__':

    aa = AutoAnki()
    print(aa.book_list)
