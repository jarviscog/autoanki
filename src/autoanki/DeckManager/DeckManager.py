import logging

import genanki
from wordfreq import word_frequency

from autoanki.DeckManager import template_decks

class DeckManager:
    """
    The class to make anki decks. Create the file using generate_deck_file()
    One of the most important concepts is the id. No matter what deck the word is in, it should have the same id so the
    same card in different decks can be remembered.
    This class makes extensive use of genanki, so understanding how genanki works
        is pretty significant for understanding this.
    """

    def __init__(self, debug_level,
                include_traditional=True,
                 include_part_of_speech=True
                 ):
        self.logger = logging.getLogger('autoanki.dckmngr')
        self.logger.setLevel(debug_level)
        self.deck = genanki.Deck(
            2020000110,
            "autoankiTesting"
        )
        self.include_pinyin_numbers = False
        self.include_number_of_strokes = False
        self.include_traditional = include_traditional 
        self.include_part_of_speech = include_part_of_speech

        self.word_frequency_filter = None

        self.book_list = []

    def settings(self,
                 include_traditional,
                 include_part_of_speech,
                 word_frequency_filter
                 ):
        """
        Configures settings for what's in the deck, and how it looks
        """
        self.include_traditional = include_traditional
        self.include_part_of_speech = include_part_of_speech 
        self.word_frequency_filter = word_frequency_filter 

    def generate_deck_file(self, words, deck_name: str, filename: str):
        """
        Generates a deck file from the database
        :param deck_name: The name of the deck to be created
        :param definitions_filename: The name of the file containing the definitions.
        :return:
        """

        # Number of valid cards that have been added to the deck
        num_of_valid_cards_added = 0

        # length = general_functions.file_len(definitions_filename)
        # self.deck.add_note()
        self.deck = genanki.Deck(
            2020000110,
            deck_name
        )

        for row in words:

            if self.word_frequency_filter:
                if self.word_frequency_filter < row['frequency']:
                    continue

            word = row["word"]

            if self.include_traditional:
                word_traditional = row["word_traditional"]
            else:
                word_traditional = ""

            if len(word) != len(word_traditional):
                self.logger.error(f"{word} and {word_traditional} should be the same length")

            # Replace all matching characters with a dash 
            formatted_word_traditional = ""
            for i in range(len(word)):
                if word[i] == word_traditional[i]:
                    formatted_word_traditional += "-"
                else:
                    formatted_word_traditional += word_traditional[i]

            if row["pinyin"]:
                pinyin = row["pinyin"]
            else:
                pinyin = row["pinyin_numbers"]
            definition = "<br>" + row["definition"]
            # word["word_id"]
            # word["word"]
            # word["word_traditional"]
            # word["word_type"]
            # word["pinyin"]
            # word["pinyin_numbers"]
            # word["number_of_strokes"]
            # word["sub_components"]
            # word["frequency"]
            # word["hsk_level"]
            # word["top_level"]]
            # word["audio_path"]
            # word["image_path"]
            # word["definition"]

            if not word:
                word = "Not found"
            if not word_traditional:
                word_traditional = "Not found"
            if not pinyin:
                pinyin = "Not found"
            if not definition:
                definition = "Not found"

            note = genanki.Note(
                model=template_decks.CHINESE_CARD_MODEL,
                tags=['autoanki'],
                fields=[word, formatted_word_traditional, pinyin, definition],
                # sort_field can be used to sort when the cards appear.
                # By default they are shown in the order they are addeed, so this is not currently used
                sort_field=1,

            )
            self.deck.add_note(note)
            num_of_valid_cards_added += 1

        if not filename.endswith(".apkg"):
            filename += ".apkg"

        genanki.Package(self.deck).write_to_file(filename)
        self.logger.info("Deck " + deck_name + " created with " + str(num_of_valid_cards_added) + " cards")
        return filename

