from abc import ABC, abstractmethod


class DatabaseManager(ABC):
    @abstractmethod
    def __init__(self, debug_level=20):
        pass

    @abstractmethod
    def get_columns(self) -> list:
        pass

    @abstractmethod
    def get_length(self) -> int:
        pass

    @abstractmethod
    def store(self, token: str):
        pass

    @abstractmethod
    def lookup(self) -> list:
        pass
