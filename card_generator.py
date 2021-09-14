import genanki
from genanki import Model
import random
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
      'afmt': '{{FrontSide}}\n\n<hr id=answer>\n{{Pinyin}}\n{{Back}}',
    },
    # {
      # 'name': 'Card 2',
      # 'qfmt': '{{FrontSide}}\n\n<hr id=answer>\n{{Pinyin}}\n{{Back}}',
      # 'afmt': '{{Front}}',
    # },
  ],
  css='.card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n',
)

def createTestDeck():
    '''
    Used for testing
    :return:
    '''

    print("Generating card")
    my_note = genanki.Note(
        model = chinese_card_model,
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

    note = None

    note = genanki.Note(
        model = chinese_card_model,
        fields=[character, pinyin, definition],
        # sort_field can be used to sort when the cards appear.
        # By default they are shown in the order they are addeed, so this is not currently used
        sort_field=1

    )

    return note

# Generates an anki file based off of a txt file of definitions
def generate_file(deck_name, definitions_filename):

    # Number of valid cards that have been added to the deck
    numOfValidCards = 0

    my_deck = genanki.Deck(
        2020000110,
        deck_name
    )

    run = True

    length = general_functions.file_len(definitions_filename)

    file = open(definitions_filename, "r", encoding='utf-8')

    # while run:
    for i in range(length):

        line = file.readline().replace('\n','')
        lineArr = line.split('&')
        char = lineArr[0]
        appearances = lineArr[1].split(':')[1]
        pinyin = lineArr[2].split(':')[1]
        pinyinNum = lineArr[3].split(':')[1]

        # print(char)
        fourExists = False
        try:
            # tries index of 5. If there is no definition then this will fail
            # p is a dummy variable
            p = lineArr[4]
            p = lineArr[4].split(':')[1]
            fourExists = True

        except IndexError:
            fourExists = False

        if fourExists:

            definition = lineArr[4].split(':')[1]
            # print('Generating note: ' + char + ' ' + pinyin)
            if definition != 'null' and definition != '(Not available);':
                note = generate_note(char, pinyin, definition)
                my_deck.add_note(note)
                numOfValidCards +=1

    genanki.Package(my_deck).write_to_file('output.apkg')
    print("Deck " + deck_name + " created with " + str(numOfValidCards) + " cards")


if __name__ == '__main__':

    generate_file('maze_runner_definitions.txt')