from abc import ABC, abstractmethod

class LanguageAdapter(ABC):
    @abstractmethod
    def __init__(self, settings):
        pass

    @abstractmethod
    def tokenize(self, text):
        pass

    @abstractmethod
    def lookup(self, token):
        pass

    @abstractmethod
    def available_settings(self):
        pass

    @abstractmethod
    def settings(self):
        pass
