from abc import ABC, abstractmethod


class Tokenizer(ABC):
    @abstractmethod
    def __init__(self, debug_level=20):
        pass

    @abstractmethod
    def tokenize(self, line: str) -> None | list[str]:
        pass
