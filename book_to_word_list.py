import pinyin as pin
import os
import general_functions

def containsAny(str, set):
    """ Check whether sequence str contains ANY of the items in set. """
    return 1 in [c in str for c in set]

NEW_FILE_EXTENTION = "_word_list.txt"


def convert(filename="full_book_with_pinyin.txt", sort_by_frequency = False, has_pinyin = True, write_frequency = True):


    if(has_pinyin):
        numOfLines = int(general_functions.file_len(filename)/2)
    else:
        numOfLines = int(general_functions.file_len(filename))

    f = open(filename, "r", encoding='utf-8')

    freqDict = {}
    missMatch = []
    missMatchCount = 0
    linePinyin = None
    for lineNum in range(numOfLines):

        if(has_pinyin):
            linePinyin = f.readline().split(" ")
        lineChars = f.readline().split(" ")

        # print(lineNum)
        # print(linePinyin)
        # print(lineChars)

        # Sometimes the pinyin and the characters from the chars to pinyin website do not line up.
        # The characters are taken from the
        if(len(lineChars) != len(linePinyin)):

            missMatch.append([lineNum,linePinyin,lineChars])
            missMatchCount +=1

            for i in range(len(lineChars)-1):
                if not containsAny(lineChars[i], "。，？！…"):
                    # print(lineChars[i] + "  " + linePinyin[i])
                    if lineChars[i] in freqDict:
                        # print("Key found: " + str(freqDict[lineChars[i]]))
                        freqDict[lineChars[i]] += 1
                    else:
                        freqDict[lineChars[i]] = 1

        else:
            for i in range(len(lineChars)-1):
                if not containsAny(lineChars[i], "。，？！…"):
                    if lineChars[i] in freqDict:
                        # print("Key found: " + str(freqDict[lineChars[i]]))
                        freqDict[lineChars[i]] += 1
                    else:
                        freqDict[lineChars[i]] = 1

    dictToWrite = None

    # Sorts the dictionary if specified
    if(sort_by_frequency):
        dictToWrite = dict(sorted(freqDict.items(), key=lambda item: item[1]))
    else:
        dictToWrite = freqDict

    # Splits the filename into a base, and an extension. Index [0] is the base
    # file.txt -> ['file', '.txt']
    # file -> ['file','']
    newFileName = os.path.splitext(filename)[0]

    newFileName = newFileName + NEW_FILE_EXTENTION

    file = open(newFileName, "w", encoding='utf-8')

    for key, value in dictToWrite.items():

        # Writes the number of times a character shows up in the book if specified

        lineToWrite = str(key)


        if(write_frequency):
            lineToWrite += ", number_of_appearances:" + str(value)

        file.write(lineToWrite + "\n")

    return newFileName

if __name__ == "__main__":

    convert()