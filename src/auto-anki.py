from DatabaseManager.DatabaseManager import DatabaseManager
from DeckManager.DeckManager import DeckManager
import os

'''

inputs
database filepath (optional)

functions
- add file (with book title)
- collect definitions
- create deck file

properties file_list


'''

# TODO Learn the logging library to stop using print statements


class AutoAnki:

    def __init__(self, database_filename="AutoAnki.db"):

        path = os.path.join('databases', database_filename)
        # print("AutoAnki: Creating...")

        self.database_filepath = path
        self.database_manager = DatabaseManager(path)
        self.deck_manager = DeckManager(path)

    def add_book_to_database(self, bookpath: str, book_name: str = 'Unnamed'):
        """
        Add a directory ful of files to the database
        :param bookpath: The filepath to the directory tat contains the files to add
        :param book_name: The name of the book being added
        :return:
        """
        print("AutoAnki: Adding book...")
        success = self.database_manager.add_book(bookpath, book_name)
        if success:
            print("AutoAnki: Added [" + bookpath + "].")
        else:
            print("AutoAnki: Was unable to add [" + book_name + "].")

    def update_definitions(self):
        """
        Updates definitions in the dictionary that haven't been found yet.
        :return:
        """
        print("AutoAnki: Updating definitions")
        # TODO check this works
        self.database_manager.complete_unfinished_records()

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
