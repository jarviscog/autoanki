import os

#from autoanki import AutoAnki
from autoanki.autoanki import AutoAnki

TEST_DB_NAME = "tests/UnitTest.db"
TEST_DECK_NAME = "tests/test.apkg"
TEST_CSV_NAME = "tests/test.csv"


class TestAutoAnki:
    @classmethod
    def setUpClass(cls):  ### run once before all test cases ###
        pass

    @classmethod
    def tearDownClass(cls):  ### run once after all test cases ###
        pass

    def setUp(self):  ### run before each test case ###
        pass

    def tearDown(self):  ### run after each test case ###
        # If the test generated a deck, delete it
        if os.path.exists(TEST_DECK_NAME):
            os.remove(TEST_DECK_NAME)  # one file at a time

    ### make sure to add => test_ <= as prefix to all test cases otherwise they won't work ###
    def test_init(self):
        aa = AutoAnki(language_code="zh", debug_level=20)
        assert aa.book_list == []

        self.tearDown()

    def test_book_list(self):
        aa = AutoAnki(language_code="zh", debug_level=20)

        # No books
        assert len(aa.book_list) == 0

        # Add book
        aa.add_book_from_string("你好。再见", "Test Book")
        assert len(aa.book_list) == 1

        # Add book incorrectly
        aa.add_book_from_file("你好。再见", "Test Book")
        assert len(aa.book_list) == 1

        self.tearDown()

    def test_example_code(self):
        # This code should match what is in the readme at all times

        aa = AutoAnki()

        # Add whatever books you want in your deck. These can be a single file, or a string
        aa.add_book_from_string("...", "My first book🍎")
        aa.add_book_from_string("short-story.txt", "My first book🍎")

        # Once all of your books are added, the definitions need to be found, and then you can create a deck!
        aa.create_deck("AutoAnki Deck", TEST_DECK_NAME)

        # self.tearDown()

    def test_add_book_from_file(self):

        aa = AutoAnki()

        # Add whatever books you want in your deck. These can be a single file, or a string
        aa.add_book_from_file(
            filepath="./tests/files/zh/chinese_novel_1.txt", book_name="Test Book"
        )

        # Once all of your books are added, the definitions need to be found, and then you can create a deck!
        aa.create_deck("AutoAnki Deck", TEST_DECK_NAME)

        self.tearDown()

    def test_add_book_from_string(self):

        aa = AutoAnki()

        # Add whatever books you want in your deck. These can be a single file, or a string
        aa.add_book_from_string(contents="你好我叫李先生", book_name="Test Add from string")

        # Once all of your books are added, the definitions need to be found, and then you can create a deck!
        aa.create_deck("AutoAnki Deck", TEST_DECK_NAME)

        self.tearDown()

    def test_add_book_from_folder(self):

        aa = AutoAnki()

        # Add whatever books you want in your deck. These can be a single file, or a string
        aa.add_book_from_folder(
            directory="./tests/files/zh/chinese_folder",
            book_name="Test Add from Folder",
        )

        # Once all of your books are added, the definitions need to be found, and then you can create a deck!
        aa.create_deck("AutoAnki Deck", TEST_DECK_NAME)

        self.tearDown()

    #    def test_add_book_from_pleco(self):
    #
    #        aa = AutoAnki()
    #
    #        aa.add_book_from_pleco(
    #            filepath="./files/zh/chinese_pleco_1.txt", book_name="Test Add from Folder"
    #        )
    #
    #        self.tearDown()

    #    def test_set_deck_settings(self):
    #        # TODO: Test each individual entry actually made it into the apkg file
    #        # TODO: Re-enable include_audio when functionality is verified
    #        # TODO: This should not be a monolith settings function. It should be multiple separate functions
    #
    #        aa = AutoAnki()
    #
    #        aa.add_book_from_pleco(
    #            filepath="./files/chinese_pleco_1.txt", book_name="Test Add from Folder"
    #        )
    #        aa.deck_settings(
    #            include_traditional=True,
    #            include_part_of_speech=True,
    #            include_audio=True,
    #            include_pinyin=True,
    #            include_zhuyin=True,
    #            hsk_filter=None,
    #            word_frequency_filter=None,
    #        )
    #
    #        aa.create_deck("AutoAnki Deck", TEST_DECK_NAME)
    #
    #        self.tearDown()

    def test_get_number_of_words(self):
        aa = AutoAnki()
        assert aa.get_number_of_words() == 0

    def test_save_empty_dictionary_as_csv(self):

        aa = AutoAnki()
        aa.save_dictionary_as_csv(TEST_CSV_NAME)

        self.tearDown()

    def test_save_dictionary_as_csv(self):

        aa = AutoAnki()

        aa.add_book_from_file(
            filepath="./tests/files/zh/chinese_novel_1.txt", book_name="Test Book"
        )
        aa.save_dictionary_as_csv(TEST_CSV_NAME)

        self.tearDown()

    def test_adding_same_book_twice(self):
        aa = AutoAnki()

        aa.add_book_from_file(
            filepath="./tests/files/zh/chinese_novel_1.txt", book_name="Test Book"
        )
        aa.add_book_from_file(
            filepath="./tests/files/zh/chinese_novel_1.txt", book_name="Test Book"
        )

    # TODO add assertions that there were no errors in ingesting the info into autoanki.
    # It will put it in the logs, but not fail the test

    # def test_hsk_filter(self):
    # def test_word_frequency_filter(self):
    # def test_card_fields_exist(self):
    # check include works on zhuyin entry, etc.
    # check include works on zhuyin data populated, etc.
