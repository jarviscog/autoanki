from abc import ABC, abstractmethod


class DatabaseManager(ABC):
    @abstractmethod
    def __init__(self, debug_level=20):
        """Contains all entries, including number of occurrences, word, and definition"""
        self.database = {}

    @abstractmethod
    def get_columns(self) -> list:
        pass

    @abstractmethod
    def get_length(self) -> int:
        pass

    @abstractmethod
    def add_contents_to_database(self, contents: str):
        pass

    @abstractmethod
    def add_book_from_string(self, contents: str, book_name: str) -> bool:
        pass

    @abstractmethod
    def add_book_from_file(self, filepath: str, book_name: str) -> bool:
        pass

    @abstractmethod
    def update_definition(self, word, params: dict):
        pass

    @abstractmethod
    def get_all_completed_definitions(self) -> dict[str, dict]:
        pass
