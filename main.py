import codecs
import pinyin as pin

def containsAny(str, set):
    """ Check whether sequence str contains ANY of the items in set. """
    return 1 in [c in str for c in set]

filename = 'full_book_with_pinyin.txt'

if __name__ == "__main__":

    # count = len(open(filename).readlines())

    f = open(filename, "r", encoding='utf-8')

    # freqDict = {'他': 1}
    freqDict = {}
    missMatch = []
    missMatchCount = 0
    for lineNum in range(7000):

        linePinyin = f.readline().split(" ")
        lineChars = f.readline().split(" ")

        # print(lineNum)
        # print(linePinyin)
        # print(lineChars)

        # if (linePinyin[-1] == '\n' and lineChars[-1] == '\n'):
        #     print("Pop")
            # linePinyin.pop(-1)
            # lineChars.pop(-1)
        # print(lineNum)

        # There are some sentences that do not play well in the translator. These are looked at separately, and can be differentiated by
        # The miss-match from pinyin to characters
        # Rather than combine the pinyin, it is much easier to split the characters （弯曲的 vs 弯曲 的， 一座 vs 一 座）
        # This may be technically incorrect, but it would take twice as long to fix, and minimal meaning is lost this way anyways
        # Many of these miss-matches may be from measure words
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

                    # print(lineChars[i] + "  " + linePinyin[i])

                    if lineChars[i] in freqDict:

                        # print("Key found: " + str(freqDict[lineChars[i]]))
                        freqDict[lineChars[i]] += 1

                    else:

                        freqDict[lineChars[i]] = 1

    sorted = dict(sorted(freqDict.items(), key=lambda item: item[1]))
    print(sorted)



    file = open("frequency.txt", "w", encoding='utf-8')

    for key, value in sorted.items():

        # file.write(str(key) + str(value) + "\n")
        file.write(str(key) + "\n")


    print("Miss-matched: ")
    for line in missMatch:

        print(line[0])
        print(line[1])
        print(line[2])
        print("")

    print(missMatchCount)