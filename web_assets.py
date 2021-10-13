from selenium.webdriver.support.select import Select
import general_functions
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
# from time import sleep


def get_pinyin(filename, headless=True):
    file_to_be_created = os.path.splitext(filename)[0] + "_pinyin.txt"

    # FIXME Remove hard-coding of downloaded filepath
    downloaded_filepath = "C:\\Users\\jarvi\\Downloads\\" + filename

    if os.path.exists(file_to_be_created):
        print('getPinyin() already done')
        return file_to_be_created

    if os.path.exists(downloaded_filepath):
        # File has already been downloaded
        print("File already downloaded")
    else:
        options = Options()
        # prefs = {"download.default_directory": "/some/path"}
        # options.add_experimental_option("prefs", prefs)
        options.headless = headless
        url = 'https://www.purpleculture.net/chinese-pinyin-converter/'
        driver = webdriver.Chrome(options=options, executable_path=str(os.getcwd() + "\\" + 'chromedriver.exe'))
        driver.get(url)
        # Grabs the definition part of the screen
        file_tab = driver.find_element_by_xpath('//*[@id="pageTwo"]/div[3]/div[1]/ul/li[2]/a')
        file_tab.click()
        upload_box = driver.find_element_by_id('txtfile')
        upload_box.send_keys(os.getcwd() + "\\" + filename)
        convert_button = driver.find_element_by_xpath('//*[@id="fileuploadform"]/div[2]/div/button[1]')
        convert_button.click()
        # Wait until file is in downloads file. Times out after 15 seconds
        for i in range(30):
            if os.path.exists(downloaded_filepath):
                break
            time.sleep(0.5)
            if i == 29:
                print("getPinyin File not downloaded correctly")
        driver.quit()

    # The file with the characters and pinyin
    pinyin_file = open(downloaded_filepath, "r", encoding='utf-8')
    # The new file to be created
    new_file_name = os.path.splitext(filename)[0] + "_pinyin.txt"

    new_file = open(new_file_name, "w", encoding='utf-8')
    length = int(general_functions.file_len(downloaded_filepath) / 2)

    for i in range(length):
        pinyin = pinyin_file.readline().strip()
        original_file = pinyin_file.readline().replace("\n", "").strip()

        new_file.write(original_file + "&pinyin:" + pinyin + "\n")

    # print('getPinyin end')

    return new_file_name


def get_pinyin_numbers(filename, headless=True):
    file_to_be_created = os.path.splitext(filename)[0] + "_pinyinNum.txt"

    print(file_to_be_created)

    # FIXME Remove hard-coding of downloaded filepath
    downloaded_filepath = "C:\\Users\\jarvi\\Downloads\\" + file_to_be_created

    if os.path.exists(file_to_be_created):
        print('getPinyinNumbers() already done')
        return file_to_be_created

    if os.path.exists(downloaded_filepath):
        #     File has already been downloaded
        print("File already downloaded")
    else:

        cut_filename = general_functions.cut(filename)

        downloaded_filepath = "C:\\Users\\jarvi\\Downloads\\" + cut_filename

        options = Options()
        options.headless = headless
        url = 'https://www.purpleculture.net/chinese-pinyin-converter/'
        driver = webdriver.Chrome(options=options, executable_path=str(os.getcwd() + "\\" + 'chromedriver.exe'))
        driver.get(url)
        # Grabs the definition part of the screen
        file_tab = driver.find_element_by_xpath('//*[@id="pageTwo"]/div[3]/div[1]/ul/li[2]/a')
        file_tab.click()
        upload_box = driver.find_element_by_id('txtfile')
        upload_box.send_keys(os.getcwd() + "\\" + cut_filename)
        select = Select(driver.find_element_by_id('toneselection_file'))
        # select by visible text
        select.select_by_value('number')

        convert_button = driver.find_element_by_xpath('//*[@id="fileuploadform"]/div[2]/div/button[1]')
        convert_button.click()
        # Wait until file is in downloads file. Times out after 15 seconds
        for i in range(30):
            if os.path.exists(downloaded_filepath):
                break
            time.sleep(0.5)
            if i == 29:
                print("getPinyinNum File not downloaded correctly")
                return
        driver.quit()

    # The file with the characters and pinyin numbers
    pinyin_file = open(downloaded_filepath, "r", encoding='utf-8')
    # The new file to be created
    new_file_name = os.path.splitext(filename)[0] + "_pinyinNum.txt"

    word_list_file = open(filename, 'r', encoding='utf-8')

    new_file = open(new_file_name, "w", encoding='utf-8')
    length = int(general_functions.file_len(downloaded_filepath) / 2)

    for i in range(length):
        pinyin = pinyin_file.readline().strip()
        original_file_cut = pinyin_file.readline().replace("\n", "").strip()
        word_list_file_line = word_list_file.readline().replace("\n", "").strip()
        new_file.write(word_list_file_line + "&pinyinNum:" + pinyin + "\n")

    # print('getPinyinNum() done')

    return new_file_name


def get_definitions(filename, new_filename, number_of_definitions_to_add, headless=True):
    """
    Takes a file with 1 definition per line, and downloads definitions for each
        filename: the file to be read from. The output file will be the filename with _definitions appended

    """
    f = open(filename, "r", encoding='utf-8')

    options = Options()
    options.headless = headless
    url = 'https://www.yellowbridge.com/chinese/dictionary.php'
    definitions_dict = {}

    while number_of_definitions_to_add > 0:

        line = f.readline()
        line_arr = line.split("&")
        chars = line_arr[0]
        has_definition = False
        for i in range(len(line_arr)):
            if line_arr[i].split(':')[0].strip() == "definition":
                print("There is a definition here " + chars)
                has_definition = True
        if has_definition:
            continue

        driver = webdriver.Chrome(options=options, executable_path=str(os.getcwd() + "\\" + 'chromedriver.exe'))
        driver.get(url)
        # Grabs the definition part of the screen
        search_box = driver.find_element_by_name('word')
        search_box.send_keys(chars)
        search_box.submit()

        try:

            main_data = driver.find_element_by_id('main_data')
            definition_data = str(main_data.get_property('innerText'))
            english_definitions = definition_data.split('\n')[1].replace('English Definition', '').replace('\t','').split(';')
            print("The definition for " + chars + " is ")

            definitions_line = ""

            for defi in english_definitions:
                definitions_line += defi + ";"

            definitions_dict[chars] = definitions_line
            print(definitions_line)

            number_of_definitions_to_add -= 1

        except Exception as e:

            print(e)
            definitions_dict[chars] = "null"

        driver.quit()

    new_file_name = new_filename
    file = open(filename, "r", encoding='utf-8')
    new_file = open(new_file_name, "w", encoding='utf-8')

    length = general_functions.file_len(filename)

    for i in range(length):

        line_to_add = file.readline().strip('\n')

        line_chars = line_to_add.strip().split('&')[0]
        # print(line_chars)
        if line_chars and line_chars in definitions_dict:
            if definitions_dict[line_chars]:
                # print('Found a match')
                line_to_add += str("&definition:" + definitions_dict[line_chars])

        line_to_add += '\n'
        # print('Line to add: ' + line_to_add)

        new_file.write(line_to_add)


def get_audio(filename):
    """
    Downloads the pinyin audio clips based off a file with a list of pinyin. Downloading all audio is 2049 files.
    Some downloaded files will be invalid because some sounds like bang5 do not exist.
    This will download a html 404 error page
    :parameter filename
    """
    print('getAudio()')
    pinyin_to_download = open(filename, "r", encoding='utf-8')
    length = general_functions.file_len(filename)

    for i in range(length):

        line = pinyin_to_download.readline().strip('\n').strip()

        # Used to check if the file has already been downloaded
        file_exists = {1: False, 2: False, 3: False, 4: False, 5: False}
        requesters = {}
        for i in range(5):

            if os.path.exists("audio\\" + line + str(i + 1) + '.mp3'):
                print('Found a file in audio: ' + line + str(i + 1))
                file_exists[i + 1] = True

            if not file_exists[i + 1]:
                requesters[i + 1] = requests.get(
                    str('https://r.yellowbridge.com/sounds/py-cbr/' + line + str(i + 1) + '.mp3'), allow_redirects=True)
                time.sleep(1)

                open(str('audio\\' + line + str(i + 1) + '.mp3'), 'wb').write(requesters[i + 1].content)
    print('getAudio() done')


def getImages(filename):
    # FIXME Finish image grabber
    return "Get definitions is a WIP"
