import logging

import genanki
from genanki import Model
from pprint import pprint

logger = logging.getLogger('autoanki')
logger.setLevel(logging.INFO)

# TODO Add this somewhere
# # All the resources for finding the
#         CHINESE_CARD_MODEL = Model(
#             1559383145,
#             'Chinese Card (autoanki)',
#             fields=[
#                 {
#                     'name': 'word',
#                     'font': 'Arial',
#                 },
#                 {
#                     'name': 'word_traditional',
#                     'font': 'Arial',
#                 },
#                 {
#                     'name': 'pinyin',
#                     'font': 'Arial',
#                 },
#                 {
#                     'name': 'definition',
#                     'font': 'Arial',
#                 },
#             ],
#             templates=[
#                 {
#                     'name': 'Card 1',
#                     'qfmt': '{{word}}\n[{{word_traditional}}]',
#                     'afmt': '{{FrontSide}}\n\n<hr id=answer>\n{{pinyin}}<br>\n{{definition}}',
#                 },
#                 # {
#                 # 'name': 'Card 2',
#                 # 'qfmt': '{{FrontSide}}\n\n<hr id=answer>\n{{Pinyin}}\n{{Back}}',
#                 # 'afmt': '{{Front}}',
#                 # },
#             ],
#             css='.card {\n font-family: arial;\n font-size: 30px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
#         )
#         my_note = genanki.Note(
#             model=CHINESE_CARD_MODEL,
#             fields=['Capital of Canada', 'Ottawa'],
#             sort_field=1
#         )
#         my_deck = genanki.Deck(
#             2023480110,
#             'Country Capitals'
#         )
#
#         my_deck.add_note(my_note)
#         genanki.Package(my_deck).write_to_file('output.apkg')

CHINESE_CARD_MODEL = Model(
    1559383145,
    'Chinese Card (autoanki)',
    fields=[
        {
            'name': 'word',
            'font': 'Arial',
        },
        {
            'name': 'word_traditional',
            'font': 'Arial',
        },
        {
            'name': 'pinyin',
            'font': 'Arial',
        },
        {
            'name': 'definition',
            'font': 'Arial',
        },
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{word}}\n[{{word_traditional}}]',
            'afmt': '{{FrontSide}}\n\n<hr id=answer>\n{{pinyin}}<br>\n{{definition}}',
        },
        # {
        # 'name': 'Card 2',
        # 'qfmt': '{{FrontSide}}\n\n<hr id=answer>\n{{Pinyin}}\n{{Back}}',
        # 'afmt': '{{Front}}',
        # },
    ],
    css='.card {\n font-family: arial;\n font-size: 30px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
)


def _create_test_deck():
    """
    Used for testing
    :return:
    """

    print("Generating card")
    my_note = genanki.Note(
        model=CHINESE_CARD_MODEL,
        fields=['Capital of Canada', 'Ottawa'],
        sort_field=1
    )
    my_deck = genanki.Deck(
        2023480110,
        'Country Capitals'
    )
    my_deck.add_note(my_note)
    genanki.Package(my_deck).write_to_file('output.apkg')


class DeckManager:
    """
    The class to make anki decks. Create the file using generate_deck_file()
    One of the most important concepts is the id. No matter what deck the word is in, it should have the same id so the
    same card in different decks can be remembered.
    This class makes extensive use of genanki, so understanding how genanki works
        is pretty significant for understanding this.
    """

    def __init__(self):
        self.deck = genanki.Deck(
            2020000110,
            "autoankiTesting"
        )
        self.include_pinyin_numbers = False
        self.include_number_of_strokes = False

        self.book_list = []

    def generate_deck_file(self, words, deck_name: str, filename: str):
        """
        Generates a deck file from the database
        :param deck_name: The name of the deck to be created
        :param definitions_filename: The name of the file containing the definitions.
        :return:
        """
        # TODO This is a legacy function. Update this to use the database, rather than text file
        # Has not been changed to use the object, which it should.

        # Number of valid cards that have been added to the deck
        num_of_valid_cards_added = 0

        # length = general_functions.file_len(definitions_filename)
        # self.deck.add_note()
        self.deck = genanki.Deck(
            2020000110,
            deck_name
        )

        for row in words:
            word = row["word"]
            word_traditional = row["word_traditional"]
            if word_traditional == 'Same':
                word_traditional = "-"
            pinyin = row["pinyin"]
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
                model=CHINESE_CARD_MODEL,
                fields=[word, word_traditional, pinyin, definition],
                # sort_field can be used to sort when the cards appear.
                # By default they are shown in the order they are addeed, so this is not currently used
                sort_field=1,

            )
            self.deck.add_note(note)

        genanki.Package(self.deck).write_to_file(filename + ".apkg")
        logger.info("Deck " + deck_name + " created with " + str(num_of_valid_cards_added) + " cards")
        return filename + ".apkg"


if __name__ == '__main__':
    maker = DeckManager()
    maker.generate_deck_file('autoanki.apkg', 'example.txt')
