import genanki
from genanki import Model

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

