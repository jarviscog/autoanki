import genanki
from genanki import Model
from pprint import pprint

# TODO Add this somewhere
# # All the resources for finding the
#         CHINESE_CARD_MODEL = Model(
#             1559383145,
#             'Chinese Card (auto-anki)',
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
    'Chinese Card (auto-anki)',
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
    The class to make anki decks. Add books to table, then create the file using generate_deck_file()
    One of the most important concepts is the id. No matter what deck the word is in, it should have the same id so the
    same card in different decks can be remembered.
    This class makes extensive use of genanki, so understanding how genanki works is pretty important for understanding this.
    """

    def __init__(self, db_filename:str):
        """

        :param db_filename: The .db file to load definitions from. The deck manager will create a
        DatabaseManager to read definitions from the database
        :param include_pinyin_numbers:  If the cards should include the pin1yin1 numbers or not
        :param include_number_of_strokes: If the cards should include the number of strokes or not
        :return:
        """
        self.deck = genanki.Deck(
            2020000110,
            "auto-ankiTesting"
        )
        self.include_pinyin_numbers = False
        self.include_number_of_strokes = False

        self.database_filename = db_filename
        # self.database_manager = DatabaseManager(db_filename)
        self.books_in_db = self.database_manager.book_list
        self.book_list = []

    def add_book(self, book_name:str):
        # TODO Add book
        # TODO Make this accept a list of books, and do some fancy SQL to reduce the number of redundant calls.
        # Otherwise, the, to, and, i... are guaranteed to be called 200 times. Way too inefficient
        # This can probably be done recursively, adding multiple books

        print("Adding book: " + book_name)

        # Check if the book is in the database
        if book_name not in self.books_in_db:
            print(f"Book [{book_name}] not found in the database")
            return
        else:
            book_definitions = self.database_manager.get_book_definitions(book_name)
            pprint(book_definitions)
            print(type(book_definitions))

            for row in book_definitions:

                dictionary_word_id = row[0]
                word = row[1]
                if row[2] is 'Same':
                    word_traditional=word
                else:
                    word_traditional = row[2]
                pinyin = row[4]
                definition = "<br>" + row[7]

                # self.deck.add_note()
                note = genanki.Note(
                    model=CHINESE_CARD_MODEL,
                    fields=[word, word_traditional, pinyin, definition],
                    # sort_field can be used to sort when the cards appear.
                    # By default they are shown in the order they are addeed, so this is not currently used
                    sort_field=1,

                )

                self.deck.add_note(note)
            print(self.deck.write_to_collection_from_addon())

    def generate_deck_file(self, deck_name, definitions_filename):
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
        file = open(definitions_filename, "r", encoding='utf-8')

        # Iterate all lines in the definitions file

        # genanki.Package(my_deck).write_to_file('output.apkg')
        print("Deck " + deck_name + " created with " + str(num_of_valid_cards_added) + " cards")


if __name__ == '__main__':
    maker = DeckManager()
    maker.generate_deck_file('auto-anki.apkg', 'example.txt')
