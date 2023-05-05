import logging

from .BookCleaner import BookCleaner
from .DatabaseManager import DatabaseManager
from .Dictionary import YellowBridgeDictionary
from .DeckManager import DeckManager

logger = logging.getLogger('autoanki')
logger.setLevel(logging.INFO)
logging.basicConfig(
    # filename='HISTORYlistener.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class AutoAnki:

    def __init__(self, database_filepath='autoanki.db'):
        """
        Creates an instance of autoanki.
        This creates a book cleaner, database connection, and deck maker
        :param database_filepath: The filepath for the database
        """
        logger.info("autoanki: Connecting to database...")

        self.database_filepath = database_filepath

        self.book_cleaner = BookCleaner()
        if not DatabaseManager.is_database(database_filepath):
            logger.info("Creating database...")
            DatabaseManager.create_autoanki_db(database_filepath)
            logger.info("Done creating database.")
        self.database_manager = DatabaseManager(database_filepath)
        self.dictionary = YellowBridgeDictionary()
        self.deck_manager = DeckManager()

        logger.info("autoanki: Connected!")

    def add_book(self, book_path: str, book_name: str = 'New Book'):
        """
        Add a directory ful of files to the database
        :param book_path: The filepath to the directory that contains the files to add. e.g. lost_prince.txt
        :param book_name: The name of the book being added e.g. "Lost Prince"
        :return:
        """

        logger.debug(f"autoanki: Adding book from [{book_path}]")

        # Clean the book
        if not self.book_cleaner.clean(book_path):
            logger.warning("autoanki: Unable to clean book [" + book_name + "].")
            return

        # Add the book to the database
        if not self.database_manager.add_book(book_path, book_name):
            logger.warning("Unable to add [" + book_name + "] to database.")
            return

        logger.info("autoanki: Added [" + book_path + "].")

    def complete_unfinished_definitions(self):
        """
        autoanki contains an internal definitions' table that is scraped from the internet. As words are added to
        autoanki, their definitions must be found. This function passively finds definitions and adds them to the table
        :return: None
        """

        # TODO Make progress par for unfinished records
        logger.info("Checking for records...")
        self.database_manager.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
        response_rows = self.database_manager.cursor.fetchall()
        while len(response_rows) > 0:
            self.database_manager.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
            response_rows = self.database_manager.cursor.fetchall()
            if len(response_rows) > 0:
                logger.info("Adding " + str(len(response_rows)) + " rows to dictionary table")
                for row in response_rows:
                    word = row[0]

                    # TODO This is a bad way of doing it, but find word is returning all of the parameters to
                    #     add to the database
                    # TODO create a dictionary that gets words from a file, not the internet
                    params = self.dictionary.find_word(word)
                    self.database_manager.complete_definition(params)

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
        # FEATURE Add more options for how the deck looks
        # FEATURE get files from only one book, not the whole database

        logger.info("Generating deck file [" + deck_name + ".apk ]")
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
