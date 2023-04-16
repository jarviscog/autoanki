
import os
import re
import sqlite3
import logging
import unicodedata


class LibraryManager:

    def __init__(self, library_path):
        if not os.path.exists(library_path):
            logging.warning("The library [", library_path, "] does not exist.")
            raise Exception("Cannot create DatabaseManager with invalid library path.")
        self.library_name = library_path
        self.book_list = []
        path = os.path.join(os.getcwd(), self.library_name)
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    @staticmethod
    def convert_to_tablename(name: str):
        """
        Converts a string to a sql-valid table name.
        :param name: The name to convert
        :return: A tablename valid for an sql table
        """
        # TODO Look more into table name conventions (- vs. _ etc.)
        #   : in sql table name?
        value = unicodedata.normalize('NFKC', name)
        # value.replace("：",":")
        value = value.replace("：", "__")
        value = re.sub(r'[^\w\s-]', '', value.lower())
        return re.sub(r'[-\s]+', '_', value).strip('-_')
