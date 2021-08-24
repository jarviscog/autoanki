from time import sleep
import general_functions
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import unidecode
import time
import os


def getAssets(filename):
    '''
    Downloads the definitions, audio, and images for all of the characters in a given file. All words should be on different lines in the file
        filename: the file to be read from. The output file will be the filename with _definitions appended

    '''
    print(getDefinitions(filename, 1))
    # print(getAudio(filename))
    # print(getImages(filename))

def getPinyin(filename):

    file_to_be_created = os.path.splitext(filename)[0] + "_pinyin.txt"

    # FIXME Remove hard-coding of downloaded filepath
    downloadedFilepath = "C:\\Users\\jarvi\\Downloads\\" + filename

    if(os.path.exists(file_to_be_created)):

        return file_to_be_created


    if os.path.exists(downloadedFilepath):
    #     File has already been downloaded
        print("File already downloaded")
    else:
        options = Options()
        prefs = {"download.default_directory": "/some/path"}
        options.add_experimental_option("prefs", prefs)
        options.headless = False
        url = 'https://www.purpleculture.net/chinese-pinyin-converter/'
        driver = webdriver.Chrome(options=options, executable_path=str(os.getcwd() + "\\" + 'chromedriver.exe'))
        driver.get(url)
        # Grabs the definition part of the screen
        file_tab = driver.find_element_by_xpath('//*[@id="pageTwo"]/div[3]/div[1]/ul/li[2]/a')
        file_tab.click()
        uploadBox = driver.find_element_by_id('txtfile')
        uploadBox.send_keys(os.getcwd() + "\\" + filename)
        convertButton = driver.find_element_by_xpath('//*[@id="fileuploadform"]/div[2]/div/button[1]')
        convertButton.click()
        #Wait until file is in downloads file. Times out after 15 seconds
        for i in range(30):
            if(os.path.exists(downloadedFilepath)):
                break
            time.sleep(0.5)
            if(i == 29):
                print("getPinyin File not downloaded correctly")
        driver.quit()

    # The file with the characters and pinyin
    pinyinFile = open(downloadedFilepath, "r", encoding='utf-8')
    # The new file to be created
    newFileName = os.path.splitext(filename)[0] + "_pinyin.txt"

    newFile = open(newFileName, "w", encoding='utf-8')
    length = general_functions.file_len(downloadedFilepath)

    for i in range(length):

        pinyin = pinyinFile.readline().strip()
        originalFile = pinyinFile.readline().replace("\n", "").strip()

        newFile.write(originalFile + "&pinyin:" + pinyin + "\n")

    # print('getPinyin end')
    return newFileName

def getDefinitions(filename, number_of_definitions_to_add):
    '''
    Takes a file with 1 definition per line, and downloads definitions for each
        filename: the file to be read from. The output file will be the filename with _definitions appended

    '''
    f = open(filename, "r", encoding='utf-8')

    options = Options()
    options.headless = False
    url = 'https://www.yellowbridge.com/chinese/dictionary.php'
    definitionsDict = {}

    while(number_of_definitions_to_add > 0):

        line = f.readline()
        lineArr = line.split("&")
        chars = lineArr[0]

        driver = webdriver.Chrome(options=options, executable_path=str(os.getcwd() + "\\" + 'chromedriver.exe'))
        driver.get(url)

        # Grabs the definition part of the screen
        search_box = driver.find_element_by_name('word')
        search_box.send_keys(chars)
        search_box.submit()
        try:

            mainData = driver.find_element_by_id('mainData')
            definitionData = str(mainData.get_property('innerText'))
            englishDefinitions = definitionData.split('\n')[1].replace('English Definition','').replace('\t', '').split(';')
            print("The definition for " + chars + " is ")

            definitionsLine = ""

            for defi in englishDefinitions:
                definitionsLine += defi + ";"

            definitionsDict[chars] = definitionsLine
            print(definitionsLine)

            number_of_definitions_to_add -=1

        except Exception as e:

            print(e)

        driver.quit()

    print("Definitions dict")
    print(definitionsDict)

    charLineDict = {}

    for key, value in definitionsDict.items():
        print(key, '->', value)

        file = open(filename, "r", encoding='utf-8')
        fileLength = general_functions.file_len(filename)
        for i in range(fileLength):

            line = file.readline()
            chars = line.split("&")[0]

            if (key == chars):

                print("Found a match on line " + str(i))

                charLineDict[chars] = i

        for key, value in definitionsDict.items():

            ogFile = open(filename, "r", encoding='utf-8')

            for i in range(int(value)):

                ogFile.readline()

                print(i)

            print("The key is " + key)
            print("The value is " + value)
            print("The key is " + key)




def getAudio(filename):
    '''
    Takes a file with 1 word + pinyin per line, and downloads definitions for each
        filename: the file to be read from. The files downloaded will be in the audio file

    '''
    charsFile = open(filename, "r", encoding='utf-8')

    charsFileLength = general_functions.file_len(filename)

    # for i in range(charsFileLength):
    for i in range(5):
        line = charsFile.readline()

        chars = line.split('&')[0].strip()
        pinyin = line.split('&')[2].split(':')[1]
        pinyinClean = unidecode.unidecode(pinyin)
        print(chars)
        print(len(chars))
        print(pinyin)
        print(pinyinClean)
        if (os.path.exists("audio\\" + pinyinClean + '1')):
            print('found 1')


        # print("Error finding")
        # print('https://r.yellowbridge.com/sounds/py-cbr/tiao3.mp3')

def getImages(filename):

    return "Get definitions is a WIP"