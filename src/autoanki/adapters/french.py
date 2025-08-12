from autoanki.adapters.base import LanguageAdapter


class FrenchAdapter(LanguageAdapter):
    def __init__(self, settings):
        raise NotImplementedError

    def tokenize(self, text):
        raise NotImplementedError

    def store(self, tokens: list[str], group_name="default"):
        raise NotImplementedError

    def _lookup(self, token) -> dict | None:
        raise NotImplementedError

    def get_number_of_entries(self) -> int:
        raise NotImplementedError

    def get_groups(self) -> list[str]:
        # TODO
        return []

    def available_settings(self) -> list:
        raise NotImplementedError

    def get_settings(self):
        raise NotImplementedError

    def get_note_fields(self, token) -> dict:
        entry = self.lookup(token)
        return {}

    def get_tokens_to_generate(self) -> dict:
        # TODO
        return {"Français": self.get_note_fields("Français")}
