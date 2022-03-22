import os
import re

GARBAGE_SENTENCES = {
    "\n",
    "",
    "。"
}

def file_len(fname):
    with open(fname, encoding='utf-8') as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def is_valid_filename(filename):
    # TODO Valid filename

    if re.findall(r'[^.A-Za-z0-9_\-\\]',filename):
        return 0
    return 1

def file_exists(filename):
    if os.path.exists(filename):
        return True
    else:
        return False

def cut(filename, extention='_cut.txt'):

    newFilename = os.path.splitext(filename)[0] + extention

    file = open(filename, "r", encoding='utf-8')

    cutFile = open(newFilename, "w", encoding='utf-8')

    length = file_len(filename)

    for i in range(length):

        chars = file.readline().split('&')[0]
        cutFile.write(chars + '\n')

    print('Cut file: ' + filename)
    print('New file: ' + newFilename)
    return newFilename

def split_filename(filename):
    """
    Removes the file extension from a filename
    :return: An array with the name and the extension
    """

    return os.path.splitext(filename)