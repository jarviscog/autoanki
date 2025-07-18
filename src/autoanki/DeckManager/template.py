from genanki import Model

CARD_MODEL = Model(
    1559383145,
    "autoanki",
    fields=[
        {
            "name": "word",
            "font": "Arial",
        },
        {
            "name": "word_alternate",
            "font": "Arial",
        },
        {
            "name": "pronunciation",
            "font": "Arial",
        },
        {
            "name": "pronunciation_alternate",
            "font": "Arial",
        },
        {
            "name": "part_of_speech",
            "font": "Arial",
            "color": "red",
        },
        {
            "name": "definition",
            "font": "Arial",
        },
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{word}}\n[{{word_alternate}}]",
            "afmt": """
            {{FrontSide}}\n
            \n
            <hr id=answer>\n
            {{pronunciation}}
            {{pronunciation_alternate}}
            <br>
            <br>
            <span style="color:gray">{{part_of_speech}}</span>
            <br>{{definition}}<br>
            """,
        },
        # {
        # 'name': 'Card 2',
        # 'qfmt': '{{FrontSide}}\n\n<hr id=answer>\n{{Pinyin}}\n{{Back}}',
        # 'afmt': '{{Front}}',
        # },
    ],
    css="""
    .card { \n 
    font-family: arial; \n 
    font-size: 30px;\n 
    text-align: center;\n 
    color: black;\n 
    background-color: white;\n
    }\n""",
)
