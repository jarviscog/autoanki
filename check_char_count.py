import main

# Adds all of the frequencies from each line in the word_list, and returns the total
def check_char_count_from_word_list(filename):

    numOfLines = main.file_len(filename)

    f = open(filename, "r", encoding='utf-8')

    total = 0

    for lineNum in range(numOfLines):

        line = f.readline()

        total += int(line.split(sep=" ")[1].split(sep="\n")[0])

    return total