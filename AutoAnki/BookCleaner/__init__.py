import os
import shutil
import glob
import warnings
from pathlib import Path

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from selenium import webdriver
from os.path import isfile, join
import time

MAX_TXT_TO_PINYIN_SIZE = 270000
CLEANED_FILES_DIRECTORY = 'cleaned_files'
COMPACTED_FILES_DIRECTORY = 'compacted_files'
# Sentences That should not be added to the completed file.
GARBAGE_SENTENCES = ['',
                     "",
                     "。",
                     "\n"]


class BookCleaner:

    def __init__(self):
        self.file_list = []
        self.bookpath = ""

    def clean(self, bookpath):
        """
        The main function of the BookCleaner class
        Cleans the files contained in the bookpath. If bookpath is a file, only clean it
        :return: The path to the cleaned files.
        """

        # If the bookpath is a file, make a folder with the same name and move the file in then run the rest of clean()
        if os.path.isfile(bookpath):
            try:
                folder = os.path.dirname(bookpath)
                dir = os.path.splitext(os.path.basename(bookpath))[0]

                # Make the new directory, move the file
                new_filepath = os.path.join(folder, dir)
                os.mkdir(new_filepath)
                shutil.copy(bookpath, new_filepath)
                bookpath = new_filepath
                print('new bookpath', bookpath)
                warnings.warn("Moved file [" + bookpath + "] to [" + new_filepath + "].")
            except FileExistsError:
                print("[" + new_filepath + "] already exists")
                return False
            except IOError:
                # print(e.message)
                print("Unable to access file")
                return False

        # Get list of files to convert
        raw_files = []
        cleaned_files = []
        compacted_files = []
        for r, d, f in os.walk(bookpath):
            for file in f:
                # Exclude files that are in compacted_files or cleaned_files directories
                in_cleaned = str(r).find(CLEANED_FILES_DIRECTORY) != -1
                in_compacted = str(r).find(COMPACTED_FILES_DIRECTORY) != -1
                if not in_cleaned and not in_compacted:
                    if '.txt' in file:
                        raw_files.append(os.path.join(r, file))

        # Check this cleaning won't be mean to the CPU
        if len(raw_files) > 50:
            yn = input("The number of files is very large. Are you sure you want to convert this many files? (Y/N)")
            if yn.lower() != 'y':
                return False

        # Now we have a list of files to convert in a directory
        if not os.path.exists(os.path.join(bookpath, CLEANED_FILES_DIRECTORY)):
            os.mkdir(os.path.join(bookpath, CLEANED_FILES_DIRECTORY))
        # if not os.path.exists(os.path.join(bookpath, COMPACTED_FILES_DIRECTORY)):
        #     os.mkdir(os.path.join(bookpath, COMPACTED_FILES_DIRECTORY))
        # FEATURE If the file is too big, this could cause memory issues this happens in a few places in AutoAnki,
        #     but alas, I am only one person and can only do so much
        # print("RAW FILES: ", raw_files)
        for file in raw_files:
            # print("Cleaning: ", file)
            # Filter one file at a time, and add it to the filtered files' directory
            # print(file)
            # Filter all files
            self._clean_file(file)
            cleaned_files.append(os.path.join(bookpath, CLEANED_FILES_DIRECTORY, os.path.basename(file)))

            # clean_file(lines)
        for file in cleaned_files:

            compacted_files.append(os.path.join(bookpath, COMPACTED_FILES_DIRECTORY, os.path.basename(file)))

        # print(raw_files)
        # print(cleaned_files)
        # print(compacted_files)

        return cleaned_files

    @staticmethod
    def _clean_file(page_path):
        """
        Takes a txt file and cleans it up, putting every sentence on a new line
        :param page_path: The txt file to clean
        :return:
        """
        filename = os.path.basename(page_path)
        bookpath = os.path.dirname(page_path)
        new_page_path = os.path.join(bookpath, CLEANED_FILES_DIRECTORY, filename)

        # Clean page file of characters that may cause issues.
        page_file = open(page_path, encoding='utf-8')
        page_sentences = page_file.read().split("\n")
        cleaned_file = open(new_page_path, "w", encoding='utf-8')

        for page_sentence in page_sentences:
            # Clean string
            page_sentence = page_sentence\
                .lstrip()\
                .rstrip()\
                .replace("  ", " ")\
                .lstrip("\"")\
                .rstrip("\"")\
                .replace("”","'")\
                .replace("　", "")\
                .replace("“","")\
                .rstrip("。")\
                .rstrip("'")
            if page_sentence not in GARBAGE_SENTENCES:
                cleaned_file.write(page_sentence + "。" + "\n")

    @staticmethod
    def _compact_file(page_path):

        print("Compacting...")
        """
        # Compacts all of the different pages in this directory into a specified size.
        # Compacted in this context means that the files are re-organized by size, not chapter/webpage
        # Some websites used have a free limit of 300kb, for example. Rather then pass all of these pages through one by
        # one, it is more efficient to compact these into 299kb files and send those.
        Currently not in use
        # :return: True if success
        """
        all_pages_text = ""

        for page_path in self.pages:
            page = open(self.bookpath + "\\" + page_path, "r", encoding="utf-8")
            for i in range(file_len(self.bookpath + "\\" + page_path)):
                all_pages_text += page.readline()

        print("Found " + str(len(self.pages)) + " pages totalling " + str(len(all_pages_text)) + " characters.")

        # Splits the all_pages_text into smaller parts and saves it to the compacted_pages directory.
        i, current_compacted_filename_number = 0, 0
        all_pages_sentences = all_pages_text.split("\n")
        current_compacted_file_size = 0
        current_compacted_file_text = ""
        while i < len(all_pages_sentences):

            current_sentence = all_pages_sentences[i]

            # If the current file has hit its limit, start a new compacted file and reset all variables
            if (len(current_sentence) + current_compacted_file_size) > self.MAX_TXT_TO_PINYIN_SIZE:
                current_compacted_filename_number += 1
                current_file = open(self.compacted_pages_directory + "\\" + "compacted-" + str(
                    current_compacted_filename_number) + ".txt", "w",
                                    encoding="utf-8")
                for line in current_compacted_file_text.split("\n"):
                    current_file.write(line + "\n")
                current_file.close()
                current_compacted_file_size = 0
                current_compacted_file_text = ""

            # Chinese characters are utf-8, meaning they are 8 bytes
            current_compacted_file_size += len(current_sentence) * 3
            current_compacted_file_text += current_sentence
            # A newline character is one byte
            current_compacted_file_size += 1
            current_compacted_file_text += "\n"

            i += 1

        current_compacted_filename_number += 1
        current_file = open(
            self.compacted_pages_directory + "\\" + "compacted-" + str(current_compacted_filename_number) + ".txt",
            "w",
            encoding="utf-8")
        for line in current_compacted_file_text.split("\n"):
            current_file.write(line + "\n")
        current_file.close()

        print("Done compacting")
        return True