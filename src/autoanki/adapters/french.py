from autoanki.adapters.base import LanguageAdapter

class FrenchAdapter(LanguageAdapter):
    def __init__(self, settings):
        pass

    def tokenize(self, text):
        pass

    def lookup(self, token):
        pass

    def available_settings(self):
        pass

    def settings(self):
        pass

    def get_note_fields(self, token):
        entry = self.lookup(token)
        pass
