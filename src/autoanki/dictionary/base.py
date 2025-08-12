from abc import ABC, abstractmethod

from autoanki.dictionary.lookup_result.base import ChineseLookupResult, LookupResult

class Dictionary(ABC):
    @abstractmethod
    def __init__(self, debug_level=20):
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def lookup(self, word) -> LookupResult | None:
        pass

class ChineseDictionary(Dictionary):

    @abstractmethod
    def __init__(self, debug_level=20):
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def lookup(self, word) -> ChineseLookupResult | None:
        pass
