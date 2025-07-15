import logging
import os

from pprint import pprint
import genanki

from autoanki.DeckManager.template import CARD_MODEL
from autoanki.DeckManager.template_zh import CHINESE_CARD_MODEL


class DeckManager:
    """
    The class to make anki decks. Create the file using generate_deck_file()
    One of the most important concepts is the id. No matter what deck the word is in, it should have the same id so the
    same card in different decks can be remembered.
    This class makes extensive use of genanki, so understanding how genanki works
        is pretty significant for understanding this.
    """

    def __init__(self, debug_level):
        self.logger = logging.getLogger("autoanki.dckmngr")
        self.logger.setLevel(debug_level)
        self.deck = genanki.Deck(2020000110, "autoankiTesting")

        self.book_list = []

    def generate_deck_file(self, words: dict[str, dict], deck_name: str, filename: str):
        """
        Generates a deck file from the database
        :param words: Dictionary of words with their fields to be included
        :param deck_name: The name of the deck to be created
        :param filename: The name of the file containing the definitions.
        :return:
        """
        __version__ = importlib.metadata.version(__package__ or __name__)

        # Number of valid cards that have been added to the deck
        num_of_valid_cards_added = 0

        self.deck = genanki.Deck(2020000110, deck_name)

        for word, word_dict in words.items():

            word_alternate = word_dict.get("word_alternate", None)
            pronunciation = word_dict.get("pronunciation", None)
            pronunciation_alternate = word_dict.get("pronunciation_alternate", None)
            part_of_speech = word_dict.get("part_of_speech", None)

            definition = word_dict.get("definition", None)
            if not definition:
                self.logger.error(f"Tried to add word with no definition. Word: {word}")
                continue

            card_tags = [f"autoanki-{__version__}"]

            note = genanki.Note(
                model=CARD_MODEL,
                tags=card_tags,
                fields=[
                    word,
                    word_alternate,
                    pronunciation,
                    pronunciation_alternate,
                    part_of_speech,
                    definition,
                ],
                # sort_field can be used to sort when the cards appear.
                # By default they are shown in the order they are added, so this is not currently used
                sort_field=1,
            )
            self.deck.add_note(note)
            num_of_valid_cards_added += 1

        if not filename.endswith(".apkg"):
            filename += ".apkg"

        # pprint("Audio files:")
        my_package = genanki.Package(self.deck)
        my_package.write_to_file(filename)

        self.logger.info(
            f"Deck [{deck_name}] created with {num_of_valid_cards_added} cards"
        )
        return filename
