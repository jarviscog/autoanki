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
    ):
        self.logger = logging.getLogger("autoanki.dckmngr")
        self.logger.setLevel(debug_level)
        self.deck = genanki.Deck(2020000110, "autoankiTesting")

        self.book_list = []

    def generate_deck_file(self, words: dict[str, dict], deck_name: str, filename: str):
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

        audio_file_list = []
        seen_audio_files = set(audio_file_list)

        for word, row in words.items():

            # Apply filters
            if self.word_frequency_filter and row["frequency"]:
                if self.word_frequency_filter < row["frequency"]:
                    continue
            if self.hsk_filter and row["hsk_level"]:
                if self.hsk_filter > row["hsk_level"]:
                    continue

            definition = "<br>" + row["definition"]
            if not definition:
                self.logger.error(f"Tried to add word with no definition. Row: {row}")
                continue

            word_traditional = "Not found"
            if self.include_traditional:
                raw_word_traditional = row["word_traditional"]
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
            if row["pinyin"]:
                pinyin = row["pinyin"]
            if self.include_pinyin_numbers:
                pinyin = row["pinyin_numbers"]
            if pinyin == "":
                pinyin = "Not found"

            # Zhuyin
            zhuyin = "<br>Not found"
            if self.include_zhuyin and row["zhuyin"]:
                zhuyin = "<br>" + row["zhuyin"]
            else:
                zhuyin = ""

            part_of_speech = row["part_of_speech"]
            if not part_of_speech:
                part_of_speech = "Not found"

            # Audio
            audio = ""
            if self.include_audio and len(word) < 5:

                # Get the filename
                audio_name = str(row["pinyin_numbers"])
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
                # By default they are shown in the order they are added, so this is not currently used
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
            f"Deck [{deck_name}] created with {num_of_valid_cards_added} cards"
        )
        return filename
