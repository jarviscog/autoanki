import time
import sqlite3
import requests
from bs4 import BeautifulSoup
import urllib.parse
import pinyin as pin_to_num


def init_database():
    connection = sqlite3.connect('../AutoAnki.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dictionary(
    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    word VARCHAR(255) NOT NULL UNIQUE,
    word_traditional VARCHAR(255),
    word_type VARCHAR(255),
    pinyin VARCHAR(255) NOT NULL,
    pinyin_numbers VARCHAR(255),
    number_of_strokes INTEGER,
    sub_components VARCHAR(255),
    frequency FLOAT,
    hsk_level VARCHAR(255),
    top_level VARCHAR(255),
    audio_path VARCHAR(255),
    image_path VARCHAR(255),
    definition VARCHAR(255),
)
    ''')


def complete_unfinished_dictionary_records():
    '''
    Scans through the database table called dictionary for rows that do not currently have a definition
    If one is found, it searches online for the definition.
    :return:
    '''

    connection = sqlite3.connect("../AutoAnki.db")
    cursor = connection.cursor()
    while True:
        print("Checking for records...")
        while True:
            cursor.execute("SELECT word FROM dictionary WHERE definition IS NULL")
            response_rows = cursor.fetchall()
            # print(response_rows)
            if len(response_rows) > 0:
                print("Adding " + str(len(response_rows)) + " rows to dictionary table")
                for row in response_rows:
                    word = row[0]
                    save_yellowbridge_data(word)
            else:
                print("No new rows to complete in dictionary table")
            time.sleep(2)


def save_yellowbridge_data(word, cache_number=None):
    '''

    :param word: The word to find on yellowbridge.
    :param cache_number: The secondary page number for a word with multiple definitions.
    :return:
    '''
    connection = sqlite3.connect("../AutoAnki.db")
    cursor = connection.cursor()
    cursor.execute("SELECT word, definition FROM dictionary WHERE word = ?", [word])
    response = cursor.fetchall()
    if len(response) == 0:
        print(word + " is not in the database")
        return
    else:
        if response[0][1] is not None:
            # print("The definition for " + word + " is already in the dictionary")
            return

    urlx = "http://www.yellowbridge.com/chinese/dictionary.php?word="
    url = urlx + urllib.parse.quote(word)
    if cache_number is not None:
        url += "&cache=" + cache_number

    response = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'})
    yellowbridge_soup = BeautifulSoup(response.content, "html.parser")

    body = yellowbridge_soup.find(id='tabbody')
    main_data = yellowbridge_soup.find(id='mainData')
    # Some definitions will show up on the page differently because they have multiple meanings/pronunciations
    # e.g 了 could be le or liao.
    # These pages actually link to other pages with a different 'cache' number
    # Default 了 page:
    # https: // www.yellowbridge.com / chinese / dictionary.php?word = % E4 % BA % 86
    # Page for le:
    # https: // www.yellowbridge.com / chinese / dictionary.php?word = % E4 % BA % 86 & cache = 5114
    # Page for laio:
    # https: // www.yellowbridge.com / chinese / dictionary.php?word = % E4 % BA % 86 & cache = 5115
    # ̶h̶i̶s̶ ̶c̶a̶n̶ ̶b̶e̶ ̶s̶o̶l̶v̶e̶d̶ ̶b̶y̶ ̶r̶e̶c̶u̶r̶s̶i̶v̶e̶l̶y̶ ̶s̶c̶r̶a̶p̶i̶n̶g̶ ̶t̶h̶e̶ ̶p̶a̶g̶e̶s̶ ̶a̶t̶ ̶t̶h̶e̶ ̶b̶o̶t̶t̶o̶m̶ ̶o̶f̶ ̶a̶n̶y̶ ̶p̶a̶g̶e̶ ̶t̶h̶a̶t̶ ̶d̶o̶e̶s̶n̶'̶t̶ ̶h̶a̶v̶e̶ ̶m̶a̶i̶n̶_̶d̶a̶t̶a̶
    # ̶S̶o̶ ̶s̶a̶v̶e̶_̶y̶e̶l̶l̶o̶w̶b̶r̶i̶d̶g̶e̶_̶d̶a̶t̶a̶(̶了)̶
    # #̶ ̶w̶i̶l̶l̶ ̶r̶e̶c̶u̶r̶s̶i̶v̶e̶l̶y̶ ̶d̶o̶
    # ̶s̶a̶v̶e̶_̶y̶e̶l̶l̶o̶w̶b̶r̶i̶d̶g̶e̶_̶d̶a̶t̶a̶(̶'̶了̶'̶,̶ ̶5̶1̶1̶4̶)̶
    # ̶s̶a̶v̶e̶_̶y̶e̶l̶l̶o̶w̶b̶r̶i̶d̶g̶e̶_̶d̶a̶t̶a̶(̶'̶了̶'̶,̶ ̶5̶1̶1̶5̶)̶
    # ̶s̶a̶v̶e̶_̶y̶e̶l̶l̶o̶w̶b̶r̶i̶d̶g̶e̶_̶d̶a̶t̶a̶(̶'̶了̶'̶,̶ ̶7̶1̶9̶5̶5̶)̶
    # ̶s̶a̶v̶e̶_̶y̶e̶l̶l̶o̶w̶b̶r̶i̶d̶g̶e̶_̶d̶a̶t̶a̶(̶'̶了̶'̶,̶ ̶6̶3̶2̶)̶
    # This means that it would have to be possible to have multiple rows in the dictionary with the same word column,
    # which breaks other parts of the code.
    # For now, we just grab the first cache number and use that one. Maybe a v2 FEATURE will be able to have multiple
    # definitions for the same character, but that is not a priority currently
    if main_data:
        yellowbridge_contains_exact_definition = True
    else:
        yellowbridge_contains_exact_definition = False
    if yellowbridge_contains_exact_definition:
        definition = simplified_script = traditional_script = pinyin = pinyin_num = part_of_speech = hsk_level = top_level = composing_words = None
        main_data = main_data.find_all('tr')
        # Collect all necessary information from the page:
        for row in main_data:
            row_info_type = row.find('td').getText()
            row_info = row.find_all('td')[1].getText()
            # print(row_info_type + ":")
            # print(row_info)
            if row_info_type == "English Definition":
                definition = row_info
            elif row_info_type == "Simplified Script":
                simplified_script = row_info
            elif row_info_type == "Traditional Script":
                traditional_script = row_info.split("P")[0]
            elif row_info_type == "Pinyin":
                pinyin = row_info
                pinyin_num = pin_to_num.get(word, format="numerical")
            elif row_info_type == "Part of Speech":
                part_of_speech = row_info
            elif row_info_type == "Proficiency Test Level":
                proficiency_level = row_info
                if "HSK=" in proficiency_level:
                    hsk_level = proficiency_level.split("HSK=")[1].split(";")[0]
                if "TOP=" in proficiency_level:
                    top_level = proficiency_level.split("TOP=")[1].split(";")[0]

        word_decomposition_soup = yellowbridge_soup.find(id='wordDecomp')
        if len(word) > 1:
            composing_words_list = word_decomposition_soup.find_all('tr')
            composing_words = ""
            for composing_word in composing_words_list:
                composing_words += str(composing_word.find_all('td')[0].find('a').getText()) + ";"

        # This is all of the information that has been collected
        # print(definition)
        # print(simplified_script)
        # print(traditional_script)
        # print(pinyin)
        # print(pinyin_num)
        # print(part_of_speech)
        # print(hsk_level)
        # print(top_level)
        # print(composing_words)
        # print("")
        # Add the information for this word to the database
        cursor.execute("UPDATE dictionary "
                       "SET word_traditional = ?, "
                       "word_type = ?,"
                       "pinyin = ?, "
                       "pinyin_numbers = ?,"
                       "sub_components = ?,"
                       "hsk_level = ?,"
                       "top_level = ?,"
                       "definition = ?"
                       "WHERE word = ?",
                       [traditional_script, part_of_speech, pinyin, pinyin_num, composing_words, hsk_level, top_level,
                        definition,
                        word])
        connection.commit()
    else:
        # print("This is not a definition page. getting all sub-pages")
        matching_results = yellowbridge_soup.find(id='multiRow')
        # Grab first row. This is usually the most common definition
        row = matching_results.find_all('tr')[0]
        # print(row.find('a'))
        href = str(row.find('a')['href'])
        # print(href)
        cache_number_from_href = href.split("word=")[1].split("&")[1].replace("cache=", "")

        save_yellowbridge_data(word, cache_number_from_href)
