import os
import pytest

from autoanki.AutoAnki import AutoAnki

TEST_DB_NAME = "tests/UnitTest.db"
TEST_DECK_NAME = "tests/test.apkg"


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
        # If the test generated a database, delete it
        if os.path.exists(TEST_DB_NAME):
            os.remove(TEST_DB_NAME)  # one file at a time
        if os.path.exists(TEST_DECK_NAME):
            os.remove(TEST_DECK_NAME)  # one file at a time

    ### make sure to add => test_ <= as prefix to all test cases otherwise they won't work ###
    def test_init(self):
        aa = AutoAnki("zh", TEST_DB_NAME, debug_level=20)
        assert aa.book_list == []
        aa.print_database_info()

        self.tearDown()

    def test_book_list(self):
        aa = AutoAnki("zh", TEST_DB_NAME, debug_level=20)

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
        if not AutoAnki.is_database(TEST_DB_NAME):
            AutoAnki.create_database(TEST_DB_NAME)

        aa = AutoAnki("zh", database_filepath="test_autoanki.db")

        # Add whatever books you want in your deck. These can be a single file, or a string
        aa.add_book_from_string("你好。我的名字是朝霖", "My first book🍎")

        # Once all of your books are added, the definitions need to be found, and then you can create a deck!
        aa.complete_unfinished_definitions()
        aa.create_deck("AutoAnki Deck", TEST_DECK_NAME)

        self.tearDown()
