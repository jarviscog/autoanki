import logging

from .BookCleaner import BookCleaner
from .DatabaseManager import DatabaseManager
from .Dictionary import CEDictionary
from .DeckManager import DeckManager

BLACK = "\u001b[30m"
RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
BLUE = "\u001b[34m"
MAGENTA = "\u001b[35m"
CYAN = "\u001b[36m"
WHITE = "\u001b[37m"
RESET = "\u001b[0m"
# Add this to see the function name:
#%(funcName)s
logging.basicConfig(
    # filename='HISTORYlistener.log',
    level=logging.DEBUG,
    format=f'{GREEN}%(asctime)s{RESET} {RED}%(levelname)8s{RESET} {YELLOW}%(name)18s{RESET}: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger('autoanki')
logger.setLevel(logging.INFO)
logger.debug(f"logger active")

logging.basicConfig(
    # filename='HISTORYlistener.log',
    level=logging.CRITICAL,
    format=f'--{GREEN}%(asctime)s{RESET} {RED}%(levelname)8s{RESET} {YELLOW}%(name)18s{RESET}: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class AutoAnki:

    def __init__(self, database_filepath='autoanki.db', logging_level=20):
        """
        Creates an instance of autoanki.
        This creates a book cleaner, database connection, and deck maker
        :param database_filepath: The filepath for the database
        :param logging_level: between 0 (DEBUG) and 50(CRITICAL)
        """
        logger.setLevel(logging_level)
        logger.info("Connecting to database...")

        self.database_filepath = database_filepath

        self.book_cleaner = BookCleaner()
        if not DatabaseManager.is_database(database_filepath):
            logger.info("Creating database...")
            DatabaseManager.create_autoanki_db(database_filepath)
            logger.info("Done creating database.")
        self.database_manager = DatabaseManager(database_filepath)
        self.dictionary = CEDictionary()
        self.deck_manager = DeckManager()

        logger.info("Connected!")

    def add_book(self, book_path: str, book_name: str = 'New Book'):
        """
        Add a directory full of files to the database
        :param book_path: The filepath to the directory that contains the files to add. e.g. lost_prince.txt
        :param book_name: The name of the book being added e.g. "Lost Prince"
        :return:
        """

        logger.debug(f"autoanki: Adding book from [{book_path}]")

        # Clean the book
        if not self.book_cleaner.clean(book_path):
            #logger.warning("autoanki: Unable to clean book [" + book_name + "].")
            return

        # Add the book to the database
        if not self.database_manager.add_book(book_path, book_name):
            #logger.warning("Unable to add [" + book_name + "] to database.")
            return

        logger.info("autoanki: Added [" + book_path + "].")

    def complete_unfinished_definitions(self):
        """
        autoanki contains an internal definitions table that is scraped from the internet. As words are added to
        autoanki, their definitions must be found. This function passively finds definitions and adds them to the table
        :return: None
        """

        # TODO Make progress bar for unfinished records
        logger.info("Checking for records...")
        self.database_manager.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
        response_rows = self.database_manager.cursor.fetchall()
        #while len(response_rows) > 0:
        self.database_manager.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
        response_rows = self.database_manager.cursor.fetchall()
        if len(response_rows) > 0:
            logger.info("Adding " + str(len(response_rows)) + " rows to dictionary table")
            for row in response_rows:
                word = row[0]

                logger.debug(f"Finding: [{word}]...")
                params = self.dictionary.find_word(word)
                if not params:
                    logger.info(f"Could not find: [{word}]")
                else:
                    self.database_manager.update_definition(params)

        else:
            logger.info("No new rows to complete in dictionary table")
            # time.sleep(2)

    @staticmethod
    def is_database(db_path):
        return DatabaseManager.is_database(db_path)

    @staticmethod
    def create_autoanki_db(db_path: str):
        DatabaseManager.create_autoanki_db(db_path)

    def create_deck(self, deck_name: str, filepath: str):
        """
        Creates a deck file in the directory of the main file.
        :return:
        """

        logger.info("Generating deck file [" + deck_name + ".apk]")
        words = self.database_manager.get_all_completed_definitions()

        deck_path = self.deck_manager.generate_deck_file(words, deck_name, filepath)
        if deck_path is None:
            logger.warning("Was not able to create deck file for [", deck_name, "]")
        else:
            logger.info("Generated deck file [" + deck_path + "]")

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


if __name__ == '__main__':

    aa = AutoAnki()
    print(aa.book_list)
