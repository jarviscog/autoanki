from abc import ABC, abstractmethod

class LanguageAdapter(ABC):
    @abstractmethod
    def __init__(self, settings):
        pass

    @abstractmethod
    def tokenize(self, text: str) -> list[str]:
        """ Tokenizes the input and returns the tokenized output
        """
        pass

    @abstractmethod
    def store(self, tokens: list[str], group_name='default'):
        """ Stores a list of tokens in the internal database

        """

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

    @abstractmethod
    def get_tokens_to_generate(self) -> dict:
        pass

