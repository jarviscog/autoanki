import os
import unittest

from autoanki.AutoAnki import AutoAnki

# @unittest.skip('Some reason')

TEST_DB_NAME = 'tests/UnitTest.db'

class TestAutoAnki(unittest.TestCase):

    @classmethod
    def setUpClass(cls): ### run once before all test cases ###
        pass

    @classmethod
    def tearDownClass(cls): ### run once after all test cases ###
        pass

    def setUp(self): ### run before each test case ###
        pass

    def tearDown(self): ### run after each test case ###
        # If the test generated a database, delete it
        if os.path.exists(TEST_DB_NAME):
          os.remove(TEST_DB_NAME) # one file at a time

    ### make sure to add => test_ <= as prefix to all test cases otherwise they won't work ###
    def test_init(self):
        aa = AutoAnki(TEST_DB_NAME, debug_level=20)
        aa.print_database_info()

    def test_book_list(self):
        aa = AutoAnki(TEST_DB_NAME, debug_level=20)

        # No books
        self.assertEqual(len(aa.book_list), 0)

        # Add book
        aa.add_book_from_string("你好。再见", "Test Book")
        self.assertEqual(len(aa.book_list), 1)

        # Add book incorrectly
        aa.add_book_from_file("你好。再见", "Test Book")
        self.assertEqual(len(aa.book_list), 1)




if __name__ == "__main__":
    unittest.main()









