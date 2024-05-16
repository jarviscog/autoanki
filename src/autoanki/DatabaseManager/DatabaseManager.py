from abc import ABC, abstractmethod
import unicodedata
import re
import os
import sqlite3


class DatabaseManager(ABC):
    @abstractmethod
    def __init__(self, debug_level=20):
        pass

    @staticmethod
    def convert_to_tablename(name: str) -> str:
        """Converts a string to a sql-valid table name"""
        value = unicodedata.normalize("NFKC", name)
        # value.replace("：",":")
        value = value.replace("：", "__")
        value = re.sub(r"[^\w\s-]", "", value.lower())
        return re.sub(r"[-\s]+", "_", value).strip("-_")

    @staticmethod
    def is_database(database_name: str):
        """Verifies integrity of AutoAnki database
        Args:
            `database_name`: Filepath of database
        """
        if not database_name.endswith(".db"):
            return False
        if not os.path.exists(database_name):
            return False
        try:
            connection = sqlite3.connect(database_name)
            cursor = connection.cursor()
            # This will fail if dictionary table does not exist
            cursor.execute("SELECT word FROM dictionary")
            connection.close()
        except sqlite3.OperationalError:
            return False
        return True

    @staticmethod
    def create_database(database_path: str) -> bool:
        pass

    @abstractmethod
    def print_info(self):
        pass

    @abstractmethod
    def add_contents_to_database(self, contents: str, table_name: str):
        pass

    @abstractmethod
    def add_book_from_string(self, contents: str, book_name: str) -> bool:
        pass

    @abstractmethod
    def add_book_from_file(self, filepath: str, book_name: str) -> bool:
        pass

    @abstractmethod
    def update_definition(self, params: list):
        pass

    @abstractmethod
    def get_all_completed_definitions(self) -> list:
        pass
