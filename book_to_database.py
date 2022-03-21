import sqlite3
import general_functions
import pynlpir

LIST_OF_TABLES_NAME = "books"
BOOK_DIRECTORY = "books/"

def convert_book_to_database(book_filename):
    """
    :param book_filename: will pull the file from ../books/book_filename
    :return: True if successful, False if error
    """

    book_filepath = BOOK_DIRECTORY + book_filename

    connection = sqlite3.connect('AutoAnki.db')
    cursor = connection.cursor()
    table_name = general_functions.split_filename(book_filename)[0]
    # table_name = "test"


    # Check to see if the table already exists. If so, this should return
    query_output = cursor.execute(f'''SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'
    ''').fetchall()
    if len(query_output) > 0:
        print(f"Table {table_name} already exists. Skipping")
        return True

    else:

        cursor.execute(f'''
            INSERT INTO {LIST_OF_TABLES_NAME} (table_name, has_pinyin, has_pinyinNumbers, has_definition, has_audio, has_image)
            VALUES (?, False, False, False, False, False)
            ''', [table_name])

        print("Flag1")
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS maze_runner (
                word_id INTEGER,
                number_of_appearances INTEGER,
                FOREIGN KEY(word_id) REFERENCES dictionary(word_id)
            )''')
        print(cursor.fetchall())

        # Start reading book
        book = open(BOOK_DIRECTORY + book_filename, "r", encoding='utf-8')

        book_length = general_functions.file_len(BOOK_DIRECTORY + book_filename)

        freq_dict = {}
        # pynlpir is used to separate the words in a sentence. 马 and 上 have separate meanings then 马上
        # https://stackoverflow.com/questions/3797746/how-to-do-a-python-split-on-languages-like-chinese-that-dont-use-whitespace
        pynlpir.open()

        # Cycle every line in the file
        for line_number in range(book_length):

            line = book.readline()
            print(line)
            token_string = pynlpir.segment(line)
            print(token_string)
            for word_details in token_string:
                if word_details in freq_dict:
                    freq_dict[word_details] = freq_dict[word_details] + 1
                else:
                    freq_dict[word_details] = 1

        # sorted_freq_dict = dict(sorted(freq_dict.items(), key=lambda item: item[1]))


        # for key in dictionary:
        #     if word not in dictionary:
        #       add word to dictionary
        #     add word to book_table with the frequency
        for key, value in freq_dict.items():
            word = key[0]
            word_type = key[1]
            frequency = value

            word_from_dictionary = cursor.execute("""SELECT word_id FROM dictionary WHERE word = ?""", [word])
            query_output = word_from_dictionary.fetchall()
            if len(query_output) == 0:
                cursor.execute('''INSERT INTO dictionary (word, word_type) VALUES (?, ?)''', [word, word_type])

            word_from_dictionary = cursor.execute(""" SELECT word_id FROM dictionary where word = ?""", [word])
            query_output = word_from_dictionary.fetchall()
            # The word_id of the current word
            word_id = query_output[0][0]

            cursor.execute(f'''INSERT INTO {table_name} (word_id, number_of_appearances) VALUES (?, ?)''', [word_id, frequency])

def check_database():

    while True:

        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
        for table in cursor:
            print(table[0])

        if input("\nDone? (Y/N)").lower().strip() != 'y':
            table_name = input("What table would you like to look at?")
            if table_name == "c":
                command = input("Enter the sql you would like to run:\n")

                try:
                    cursor.execute(command)
                except sqlite3.Error as error:
                    print(error)
            else:
                cursor.execute(f'SELECT * FROM {table_name}')
                print_table(cursor.fetchall())
        else:
            return

        print("\nDone.")
