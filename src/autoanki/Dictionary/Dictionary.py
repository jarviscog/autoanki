from abc import ABC, abstractmethod


class Dictionary(ABC):

    @abstractmethod
    def __init__(self, debug_level=20):
        pass

    @abstractmethod
    def find_word(self, word:str) -> None | list[str]:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

