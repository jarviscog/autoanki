import genanki
from genanki import Model
# import random
import general_functions

chinese_card_model = Model(
    1559383145,
    'Chinese Card (AutoAnki)',
    fields=[
        {
            'name': 'Front',
            'font': 'Arial',
        },
        {
            'name': 'Pinyin',
            'font': 'Arial',
        },
        {
            'name': 'Back',
            'font': 'Arial',
        },
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}',
            'afmt': '{{FrontSide}}\n\n<hr id=answer>\n{{Pinyin}}<br>\n{{Back}}',
        },
        # {
        # 'name': 'Card 2',
        # 'qfmt': '{{FrontSide}}\n\n<hr id=answer>\n{{Pinyin}}\n{{Back}}',
        # 'afmt': '{{Front}}',
        # },
    ],
    css='.card {\n font-family: arial;\n font-size: 30px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
)


def create_test_deck():
    """
    Used for testing
    :return:
    """

    print("Generating card")
    my_note = genanki.Note(
        model=chinese_card_model,
        fields=['Capital of Canada', 'Ottawa'],
        sort_field=1
    )
    my_deck = genanki.Deck(
        2023480110,
        'Country Capitals'
    )
    my_deck.add_note(my_note)
    genanki.Package(my_deck).write_to_file('output.apkg')


def generate_note(character, pinyin, definition):

    note = genanki.Note(
        model=chinese_card_model,
        fields=[character, pinyin, definition],
        # sort_field can be used to sort when the cards appear.
        # By default they are shown in the order they are addeed, so this is not currently used
        sort_field=1,

    )

    return note

class DeckMaker:

    def __int__(self):
        # TODO __init__()
        self.book_list = None

    def add_book(self):
        # TODO Add book
        print("Adding book")

    def generate_deck_file(deck_name, definitions_filename):
        """
        Generates a deck file from the database
        :param deck_name: The name of the deck to be created
        :param definitions_filename: The name of the file containing the definitions.
        :return:
        """
        # TODO This is a legacy function. Update this to use the database, rather than text file
        # Number of valid cards that have been added to the deck
        num_of_valid_cards_added = 0

        my_deck = genanki.Deck(
            2020000110,
            deck_name
        )

        length = general_functions.file_len(definitions_filename)
        file = open(definitions_filename, "r", encoding='utf-8')

        # Iterate all lines in the definitions file
        for i in range(length):

            line = file.readline().replace('\n', '')
            line_arr = line.split('&')
            char = line_arr[0]
            appearances = line_arr[1].split(':')[1]
            pinyin = line_arr[2].split(':')[1]
            pinyin_num = line_arr[3].split(':')[1]

            # print(char)
            try:
                # tries index of 5. If there is no definition then this will fail
                # p is a dummy variable
                p = line_arr[4]
                p = line_arr[4].split(':')[1]
                definitions_exist = True

            except IndexError:
                definitions_exist = False

            if definitions_exist:

                definitions = line_arr[4].split(':')[1]
                # print('Generating note: ' + char + ' ' + pinyin)
                if definitions != 'null' and definitions != '(Not available);':

                    definition_string = '<br>'

                    for definition in definitions.split(';'):

                        # Anki uses html to format cards
                        definition_string += definition
                        definition_string += "<br>"

                    note = generate_note(char, pinyin, definition_string)
                    my_deck.add_note(note)
                    num_of_valid_cards_added += 1

        genanki.Package(my_deck).write_to_file('output.apkg')
        print("Deck " + deck_name + " created with " + str(num_of_valid_cards_added) + " cards")


if __name__ == '__main__':
    maker = DeckMaker()
    maker.generate_deck_file('AutoAnki.apkg', 'example.txt')
