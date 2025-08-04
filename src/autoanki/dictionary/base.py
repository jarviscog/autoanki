from abc import ABC, abstractmethod

class Dictionary(ABC):
    @abstractmethod
    def __init__(self, debug_level=20):
        pass

    @abstractmethod
    def name(self, debug_level=20):
        pass

    @abstractmethod
    def description(self, debug_level=20):
        pass

    @abstractmethod
    def link(self, debug_level=20):
        pass

    @abstractmethod
    def find_word(self, word: str) -> None | dict[str, str]:
        pass

    @abstractmethod
    def size(self) -> int:
        pass
