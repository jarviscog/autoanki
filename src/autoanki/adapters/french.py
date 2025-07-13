from autoanki.adapters.base import LanguageAdapter

class FrenchAdapter(LanguageAdapter):
    def __init__(self, settings):
        pass

    def tokenize(self, text):
        pass

    def store(self, tokens: list[str], group_name='default'):
        pass

    def lookup(self, token):
        pass

    def available_settings(self) -> dict:
        return {}

    def settings(self):
        pass

    def get_note_fields(self, token) -> dict:
        entry = self.lookup(token)
        return {}

    def get_tokens_to_generate(self) -> dict:
        # TODO
        return {
            'Français': self.get_note_fields('Français')
        }

