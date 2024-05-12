import logging

from autoanki.BookCleaner import BookCleaner
from autoanki.DatabaseManager import DatabaseManager
from autoanki.Dictionary import CEDictionary
from autoanki.DeckManager import DeckManager
from autoanki.Tokenizer import ChineseTokenizer

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
    format=f'{GREEN}%(asctime)s{RESET} {RED}%(levelname)8s{RESET} {YELLOW}%(name)-16s{RESET}: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class AutoAnki:

    def __init__(self, database_filepath='autoanki.db', debug_level=20, force=False, dictionary=None):
        """
        Creates an instance of autoanki.
        This creates a book cleaner, database connection, dictioary connection, and deck maker
        :param database_filepath: The filepath for the database
        :param logging_level: between 0 (DEBUG) and 50(CRITICAL)
        :param `force`: Skip conformations for cleaning large numbers of files
        """
        self.logger = logging.getLogger('autoanki')
        self.logger.setLevel(debug_level)
        self.logger.debug(f"logger active")
        self.logger.info("Connecting to database...")

        self.force = force
        self.book_cleaner = BookCleaner(debug_level, self.force)

        if dictionary:
            self.logger.info("Using custom dictionary")
        else:
            self.dictionary = CEDictionary(debug_level)

        self.database_filepath = database_filepath
        if not DatabaseManager.is_database(database_filepath):
            self.logger.info("Creating database...")
            DatabaseManager.create_database(database_filepath)
            self.logger.info("Done creating database.")
        self.database_manager = DatabaseManager(database_filepath, debug_level)

        self.deck_manager = DeckManager(debug_level)

        self.logger.info("Connected!")

    def add_book(self, book_path: str, book_name: str = 'New Book'):
        """
        Add a directory full of files to the database
        :param book_path: The filepath to the directory that contains the files to add. e.g. lost_prince.txt
        :param book_name: The name of the book being added e.g. "Lost Prince"
        :return:
        """
        self.logger.debug(f"autoanki: Adding book from [{book_path}]")

        # Clean the book
        # if not self.book_cleaner.clean(book_path):
            # self.logger.warning("autoanki: Unable to clean book [" + book_name + "].")
            # return

        # Add the book to the database
        if not self.database_manager.add_book(book_path, book_name):
            self.logger.warning("Unable to add [" + book_name + "] to database.")
            return

        self.logger.info("autoanki: Added [" + book_path + "].")

    def complete_unfinished_definitions(self):
        """
        autoanki contains an internal definitions table that is scraped from the internet. As words are added to
        autoanki, their definitions must be found.
        This function finds definitions and adds them to the table
        """
        # TODO Make progress bar for unfinished records
        self.logger.info("Checking for records...")
        self.database_manager.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
        response_rows = self.database_manager.cursor.fetchall()
        if len(response_rows) == 0:
            self.logger.info("No new rows to complete in dictionary table")
            return

        self.logger.info("Adding " + str(len(response_rows)) + " rows to dictionary table")
        self.tokenizer = ChineseTokenizer()
        for row in response_rows:
            word = str(row[0])

            # self.logger.debug(f"Finding: [{word}]")
            # self.logger.debug("Trying local dictionary...")
            params = self.dictionary.find_word(word)
            if params:
                # self.logger.debug(f"✅Found: [{params[8]}]")
                self.database_manager.update_definition(params)
                continue

            self.logger.info(f"❌Could not find: [{word}]")

    def deck_settings(self,
                      inclue_traditional = True,
                      inclue_part_of_speech = True,
                      word_frequency_filter = None,
                      ):
        """Configures settings for what's in the deck, and how it looks"

        `word_frequency_filter`: Float between 0 and 1. 1 being every word is included, 0 being none are included
        """
        self.deck_manager.settings(
            inclue_traditional,
            inclue_part_of_speech,
            word_frequency_filter,
        )

    def print_database_info(self):
        self.database_manager.print_info()

    @staticmethod
    def is_database(db_path):
        return DatabaseManager.is_database(db_path)

    @staticmethod
    def create_database(db_path: str):
        DatabaseManager.create_database(db_path)

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
            self.logger.warning("Was not able to create deck file for [", deck_name, "]")
        else:
            self.logger.info("Generated deck file [" + deck_path + "]")

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


