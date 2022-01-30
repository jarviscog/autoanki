import os
import general_functions


def contains_any(string, check_set):
    """ Check whether sequence str contains ANY of the items in set. """
    return 1 in [c in string for c in check_set]


def convert(filename, sort_by_frequency=False, write_frequency=True,
            extension="_word_list.txt"):

    num_of_lines = int(general_functions.file_len(filename))


    for lineNum in range(num_of_lines):

        line_chars = f.readline().split(" ")

        # Sometimes the pinyin and the characters from the chars to pinyin website do not line up.
        # The characters are taken from the

        for i in range(len(line_chars) - 1):
            if not contains_any(line_chars[i], "。，？！…、·"):
                if line_chars[i] in freq_dict:
                    # print("Key found: " + str(freq_dict[line_chars[i]]))
                    freq_dict[line_chars[i]] += 1
                else:
                    freq_dict[line_chars[i]] = 1

    # Sorts the dictionary if specified
    if sort_by_frequency:
        dict_to_write = dict(sorted(freq_dict.items(), key=lambda item: item[1]))
    else:
        dict_to_write = freq_dict

    new_file_name = os.path.splitext(filename)[0]

    new_file_name = new_file_name + extension

    file = open(new_file_name, "w", encoding='utf-8')

    for key, value in dict_to_write.items():

        # Writes the number of times a character shows up in the book if specified

        line_to_write = str(key)

        if write_frequency:
            line_to_write += "& number_of_appearances:" + str(value)

        file.write(line_to_write + "\n")

    return new_file_name


if __name__ == "__main__":

    print("book_to_word_list.txt")
    # convert()
