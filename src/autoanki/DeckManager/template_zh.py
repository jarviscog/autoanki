from genanki import Model

CHINESE_CARD_MODEL = Model(
    1559383145,
    "autoanki-chinese",
    fields=[
        {
            "name": "word",
            "font": "Arial",
        },
        {
            "name": "word_traditional",
            "font": "Arial",
        },
        {
            "name": "pinyin",
            "font": "Arial",
        },
        {
            "name": "zhuyin",
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
            "qfmt": "{{word}}\n[{{word_traditional}}]",
            "afmt": """
            {{FrontSide}}\n
            \n
            <hr id=answer>\n
            {{pinyin}}
            {{zhuyin}}
            <br>
            <br>
            <span style="color:gray">{{part_of_speech}}</span>
            {{definition}}<br>
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
