import logging
import os

import genanki
from wordfreq import word_frequency
from pydub import AudioSegment
from pprint import pprint

from autoanki.DeckManager import template_decks


class DeckManager:
    """
    The class to make anki decks. Create the file using generate_deck_file()
    One of the most important concepts is the id. No matter what deck the word is in, it should have the same id so the
    same card in different decks can be remembered.
    This class makes extensive use of genanki, so understanding how genanki works
        is pretty significant for understanding this.
    """

    def __init__(
        self,
        debug_level,
        include_traditional=True,
        include_pinyin=True,
        include_pinyin_numbers=False,
        include_zhuyin=False,
        include_part_of_speech=True,
        include_audio=False,
        word_frequency_filter=None,
        hsk_filter=None,
    ):
        self.logger = logging.getLogger("autoanki.dckmngr")
        self.logger.setLevel(debug_level)
        self.deck = genanki.Deck(2020000110, "autoankiTesting")

        self.include_pinyin = include_pinyin
        self.include_pinyin_numbers = include_pinyin_numbers
        self.include_zhuyin = include_zhuyin
        self.include_traditional = include_traditional
        self.include_audio = include_audio
        self.include_part_of_speech = include_part_of_speech

        self.word_frequency_filter = word_frequency_filter
        self.hsk_filter = hsk_filter

        self.book_list = []

    def settings(
        self,
        include_traditional,
        include_part_of_speech,
        include_audio,
        include_pinyin,
        include_zhuyin,
        word_frequency_filter,
        hsk_filter,
    ):
        """
        Configures settings for what's in the deck, and how it looks
        """
        self.include_traditional = include_traditional
        self.include_part_of_speech = include_part_of_speech
        self.include_audio = include_audio
        self.logger.debug(f"Audio: {self.include_audio}")
        self.include_pinyin = include_pinyin
        self.include_zhuyin = include_zhuyin
        self.word_frequency_filter = word_frequency_filter
        self.hsk_filter = hsk_filter

    def generate_deck_file(self, words: list[dict], deck_name: str, filename: str):
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
        self.deck = genanki.Deck(2020000110, deck_name)
        WORD = 1
        WORD_TRADITIONAL = 2
        PINYIN = 3
        PINYIN_NUMBERS = 4
        ZHUYIN = 5
        JYUTPING = 6
        PART_OF_SPEECH = 7
        NUMBER_OF_STROKES = 8
        SUB_COMPONENTS = 9
        DEFINITION = 10
        FREQUENCY = 11
        HSK_LEVEL = 12
        TOCFL_LEVEL = 13
        AUDIO_PATH = 14
        IMAGE_PATH = 15
        CHARACTER_GRAPHIC = 16
        EXAMPLES = 17

        audio_file_list = []
        seen_audio_files = set(audio_file_list)

        for row in words:

            # Apply filters
            if self.word_frequency_filter and row[FREQUENCY]:
                if self.word_frequency_filter < row[FREQUENCY]:
                    continue
            if self.hsk_filter and row[HSK_LEVEL]:
                if self.hsk_filter > row[HSK_LEVEL]:
                    continue

            word = row[WORD]
            if not word:
                self.logger.error(f"Tried to add word with no word. Row: {row}")
                continue
            definition = "<br>" + row[DEFINITION]
            if not definition:
                self.logger.error(f"Tried to add word with no definition. Row: {row}")
                continue

            word_traditional = "Not found"
            if self.include_traditional:
                raw_word_traditional = row[WORD_TRADITIONAL]
                if raw_word_traditional:
                    if len(word) != len(raw_word_traditional):
                        self.logger.error(
                            f"{word} and {raw_word_traditional} should be the same length"
                        )
                    # Replace all matching characters with a dash
                    word_traditional = ""
                    for i in range(len(word)):
                        if word[i] == raw_word_traditional[i]:
                            word_traditional += "-"
                        else:
                            word_traditional += raw_word_traditional[i]

            # Pinyin
            pinyin = ""
            if row[PINYIN]:
                pinyin = row[PINYIN]
            if self.include_pinyin_numbers:
                pinyin = row[PINYIN_NUMBERS]
            if pinyin == "":
                pinyin = "Not found"

            # Zhuyin
            zhuyin = "<br>Not found"
            if self.include_zhuyin and row[ZHUYIN]:
                zhuyin = "<br>" + row[ZHUYIN]
            else:
                zhuyin = ""

            part_of_speech = row[PART_OF_SPEECH]
            if not part_of_speech:
                part_of_speech = "Not found"

            # Audio
            audio = ""
            if self.include_audio and len(word) < 5:

                # Get the filename
                audio_name = str(row[PINYIN_NUMBERS])
                audio_name.replace("ü", "u")
                audio_name = audio_name.replace(" ", "")
                audio_name = audio_name.replace("'", "")

                audio_file = audio_name + ".mp3"

                # If it's not there, create it from spliced files
                path_to_audio_file = os.path.join(
                    os.path.dirname(__file__), "mandarin_sounds", audio_file
                )
                path_to_spliced_audio_file = os.path.join(
                    os.path.dirname(__file__), "mandarin_sounds", "spliced", audio_file
                )
                self.logger.debug(f"Audio file path: {path_to_audio_file}")
                if os.path.exists(path_to_audio_file):
                    audio_path = path_to_audio_file
                elif os.path.exists(path_to_spliced_audio_file):
                    audio_path = path_to_spliced_audio_file
                else:
                    audio_path = create_chinese_audio_file(audio_name)

                audio = f"[sound:{audio_file}]"

                # Look for the audio file
                if audio_path not in seen_audio_files:
                    seen_audio_files.add(audio_path)
                    audio_file_list.append(audio_path)

            card_tags = ["autoanki"]

            note = genanki.Note(
                model=template_decks.CHINESE_CARD_MODEL,
                tags=card_tags,
                fields=[
                    word,
                    word_traditional,
                    pinyin,
                    audio,
                    zhuyin,
                    part_of_speech,
                    definition,
                ],
                # sort_field can be used to sort when the cards appear.
                # By default they are shown in the order they are addeed, so this is not currently used
                sort_field=1,
            )
            self.deck.add_note(note)
            num_of_valid_cards_added += 1

        if not filename.endswith(".apkg"):
            filename += ".apkg"

        # pprint("Audio files:")
        # pprint(audio_file_list)
        my_package = genanki.Package(self.deck)
        my_package.media_files = audio_file_list
        my_package.write_to_file(filename)

        self.logger.info(
            "Deck "
            + deck_name
            + " created with "
            + str(num_of_valid_cards_added)
            + " cards"
        )
        return filename


def create_chinese_audio_file(audio_name: str) -> str:
    """Create a chinese audio file by splicing other files together
    This function assumes the folder with all of the base mp3s is in the right spot
    Return: path to the audio file
    """

    # print("Audio: " + audio_name)
    audio_name = audio_name.replace(" ", "")
    audio_path = os.path.join(
        os.path.dirname(__file__), "mandarin_sounds", "spliced", audio_name + ".mp3"
    )

    file_list = []
    current_pinyin = ""
    for char in audio_name:
        current_pinyin += char
        if char.isdigit():
            current_pinyin = current_pinyin.replace("ü", "u")
            current_pinyin = current_pinyin.strip()
            file_list.append(current_pinyin)
            current_pinyin = ""

    # print(file_list)

    # If the pre-made list doesnt have a 5th tone file, just use first tone
    for i, file in enumerate(file_list):
        full_path = os.path.join(
            os.path.dirname(__file__), "mandarin_sounds", file_list[0] + ".mp3"
        )
        if not os.path.exists(full_path):
            file_list[i] = file.replace("5", "1")

    try:
        # print("Grabbing files...")
        file_path = os.path.join(
            os.path.dirname(__file__), "mandarin_sounds", file_list[0] + ".mp3"
        )
        # print(file_path)
        total_sound = AudioSegment.from_mp3(file_path)
        for file in file_list[1:]:
            file_to_grab = os.path.join(
                os.path.dirname(__file__), "mandarin_sounds", file + ".mp3"
            )
            # print(file_to_grab)
            sound = AudioSegment.from_mp3(file_to_grab)
            total_sound += sound

        # Writing mp3 files is a one liner
        total_sound.export(audio_path, format="mp3")

        print("This will be saved to: " + audio_path)
        print()

        return audio_path

    except Exception as e:
        print(f"Error with {file_list}")
        print(e)
        return ""
