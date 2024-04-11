import logging
import jieba

from autoanki.Dictionary.YellowBridgeDictionary import YellowBridgeDictionary

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
logging.basicConfig(
    # filename='HISTORY.log',
    level=logging.WARNING,
    format=f'{GREEN}%(asctime)s{RESET} {RED}%(levelname)8s{RESET} {YELLOW}%(name)16s{RESET}: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class AutoAnki:

    def __init__(self, database_filepath='autoanki.db', debug_level=20, force=False):
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

        self.dictionary = CEDictionary(debug_level)
        self.online_dictionary = YellowBridgeDictionary(debug_level)

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
        if not self.book_cleaner.clean(book_path):
            # self.logger.warning("autoanki: Unable to clean book [" + book_name + "].")
            return

        # Add the book to the database
        if not self.database_manager.add_book(book_path, book_name):
            self.logger.warning("Unable to add [" + book_name + "] to database.")
            return

        self.logger.info("autoanki: Added [" + book_path + "].")

    def complete_unfinished_definitions(self):
        """
        autoanki contains an internal definitions table that is scraped from the internet. As words are added to
        autoanki, their definitions must be found.
        This function passively finds definitions and adds them to the table
        :return: None
        """

        # TODO Make progress bar for unfinished records
        self.logger.info("Checking for records...")
        self.database_manager.cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
        response_rows = self.database_manager.cursor.fetchall()
        if len(response_rows) > 0:
            self.logger.info("Adding " + str(len(response_rows)) + " rows to dictionary table")
            for row in response_rows:
                word = str(row[0])

                # self.logger.info(f"Finding: [{word}]...")

                # self.logger.debug("Trying local dictionary...")
                params = self.dictionary.find_word(word)
                if params:
                    # self.logger.debug(f"✅Found: [{params[8]}]")
                    self.database_manager.update_definition(params)
                    continue

                subwords = jieba.cut(word)
                if len(next(subwords)) == len(word):
                    pass 
                else: 
                    self.database_manager.remove_word(word)
                    subwords = jieba.cut(word)
                    self.logger.debug(f"✅Splitting and inserting: [{word}]")
                    for subword in subwords:
                        self.database_manager.insert_word(subword)
                        params = self.dictionary.find_word(subword)
                        if params:
                            self.logger.debug(f"✅  Found: [{params[8]}]")
                            self.database_manager.update_definition(params)
                        else:
                            self.logger.debug(f"❌Could not find: [{word}]")

                    continue

                CHINESE_NUMBERS = "第一二两三四五五六七八九十百千万满"
                # Remove all numbers from the front
                # Lots of the words follow the following format:
                #   Number + Subject
                old_word = "" 
                temp_word = word
                while old_word != temp_word:
                    old_word = temp_word 
                    if len(temp_word) == 0:
                        break
                    if temp_word[0] in CHINESE_NUMBERS:
                        temp_word = temp_word[1:]
                params = self.dictionary.find_word(temp_word)
                if params:
                    self.database_manager.remove_word(word)
                    self.database_manager.insert_word(temp_word)
                    self.logger.debug(f"✅  Found: [{params[8]}]")
                    self.database_manager.update_definition(params)
                    continue

                # Can we remove some modifiers and get it?
                stripped_word = word.lstrip('小')
                stripped_word = stripped_word.lstrip('大')
                stripped_word = stripped_word.lstrip('这')
                stripped_word = stripped_word.lstrip('那')
                stripped_word = stripped_word.lstrip('不')
                stripped_word = stripped_word.lstrip('几')
                stripped_word = stripped_word.lstrip('无')
                stripped_word = stripped_word.lstrip('没')
                stripped_word = stripped_word.lstrip('全')
                stripped_word = stripped_word.lstrip('上')
                stripped_word = stripped_word.lstrip('下')
                stripped_word = stripped_word.lstrip('太')
                params = self.dictionary.find_word(stripped_word)
                if params:
                    self.database_manager.remove_word(word)
                    self.database_manager.insert_word(stripped_word)
                    self.logger.debug(f"✅  Found: [{params[8]}]")
                    self.database_manager.update_definition(params)
                    continue

                # TODO 2 repeated, 1
                # 点点头
                # 长长的

                # TODO 的 at the end

                # TODO 2 repeated, 2 repeated
                # 起起伏伏

                # Nuclear option. TODO
                if len(word) == 2:
                    self.database_manager.remove_word(word)

                    self.database_manager.insert_word(word[0])
                    params = self.dictionary.find_word(word[0])
                    if params:
                        self.logger.debug(f"✅  Found: [{params[8]}]")
                        self.database_manager.update_definition(params)
                        

                    self.database_manager.insert_word(word[1])
                    params = self.dictionary.find_word(word[1])
                    if params:
                        self.logger.debug(f"✅  Found: [{params[8]}]")
                        self.database_manager.update_definition(params)


                # self.logger.debug("Trying YellowBridge...")
                # params = self.online_dictionary.find_word(word)
                # if params:
                    # self.logger.debug(f"✅Found: [{word}]")
                    # self.database_manager.update_definition(params)
                    # continue

                self.logger.debug(f"❌Could not find: [{word}]")

        else:
            self.logger.info("No new rows to complete in dictionary table")

    def deck_settings(self,
                      inclue_traditional = True, 
                      inclue_part_of_speech = True, 
                      ):
        """
        Configures settings for what's in the deck, and how it looks
        """


        self.deck_manager.settings(
            inclue_traditional,
            inclue_part_of_speech, 
        )


        pass

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


if __name__ == '__main__':

    # This is where the command line tool will be put
    # Parse args
    # parser = argparse.ArgumentParser(description='This is a new command-line tool')

    # Input files
    aa = AutoAnki()

    # Output deck
    # aa.create_deck()
    print(aa.book_list)
