from abc import ABC, abstractmethod

class LanguageAdapter(ABC):
    @abstractmethod
    def __init__(self, settings):
        pass

    @abstractmethod
    def tokenize(self, text) -> list[str]:
        pass

    @abstractmethod
    def lookup(self, token) -> dict:
        pass

    @abstractmethod
    def available_settings(self) -> dict:
        pass

    @abstractmethod
    def settings(self):
        pass

    @abstractmethod
    def get_note_fields(self, token) -> dict:
        pass
