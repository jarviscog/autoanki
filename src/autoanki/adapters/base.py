from abc import ABC, abstractmethod


"""
All resources specific to a given language
"""


class LanguageAdapter(ABC):
    @abstractmethod
    def __init__(self, settings: dict = {}):
        pass

    @abstractmethod
    def tokenize(self, text: str) -> list[str]:
        """Tokenizes the input and returns the tokenized output"""
        pass

    @abstractmethod
    def store(self, tokens: list[str], group_name="default"):
        """Stores a list of tokens in the internal database"""

    @abstractmethod
    def get_number_of_entries(self) -> int:
        pass

    @abstractmethod
    def lookup(self, token) -> dict | None:
        pass

    @abstractmethod
    def get_groups(self) -> list[str]:
        pass

    @abstractmethod
    def available_settings(self) -> dict:
        pass

    @abstractmethod
    def get_settings(self) -> dict:
        """Returns the current value for each setting"""
        pass

    @abstractmethod
    def get_note_fields(self, token) -> dict:
        """Gets the card fields for a given input token
        This will be language-agnostic. The output dictionary will have the following structure:
        [
            "word",
            "word_alternate",
            "pronunciation",
            "pronunciation_alternate",
            "part_of_speech",
            "definition",
        ]

        """
        # TODO the code should be self documenting (make this into a class?)
        pass

    @abstractmethod
    def get_tokens_to_generate(self) -> dict:
        """
        Get all tokens to turn into cards, after filters and missing definitions
        """
        pass
