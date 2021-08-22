from time import sleep

import requests


def getDefinitions(filename):
    '''
    Takes a file with 1 definition per line, and downloads definitions for each
        filename: the file to be read from. The output file will be the filename with _definitions appended

    '''

    print("Getting definitions...")

    f = open(filename, "r", encoding='utf-8')

    for i in range(1):
        line = f.readline()
        lineArr = line.split(",")

        chars = lineArr[0]

        url = 'https://www.yellowbridge.com/chinese/dictionary.php'

        query = {'word': chars}
        response = requests.get(url, params=query)
        print(response.content.decode())