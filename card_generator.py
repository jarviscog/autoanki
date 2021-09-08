import genanki

def createTestCard():

    print("Generating card")
    my_note = genanki.Note(
        model = genanki.BASIC_MODEL,
        fields=['Capital of Canada', 'Ottawa']
    )
    my_deck = genanki.Deck(
        2023480110,
        'Country Capitals')

    my_deck.add_note(my_note)

    genanki.Package(my_deck).write_to_file('output.apkg')


if __name__ == '__main__':

    createTestCard()