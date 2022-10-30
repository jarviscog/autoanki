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
            warnings.warn("Moved file [" + bookpath + "] to folder with the same name.")
            try:
                folder = os.path.dirname(bookpath)
                dir = os.path.splitext(os.path.basename(bookpath))[0]
                # print('dir', dir)
                file = os.path.basename(bookpath)
                # Make the new directory, move the file
                new_filepath = os.path.join(folder, dir)
                os.mkdir(new_filepath)
                shutil.copy(bookpath, new_filepath)
                bookpath = new_filepath
                print('new bookpath', bookpath)
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


# This is old code, and will be replaced with nlp, and some moved to DatabaseManager

#     # In bytes. One utf-8 character is 3 bytes. One ASCII character is 1 byte
#     # This could be a more exact number (1024b not 1000b), but better to be on the low end then the website refuse.
#
#     def _get_pinyin_of_pages(self, headless=True):
#         """
#         Downloads the pinyin of the characters, and stores that with the original characters in pinyin_pages
#         :param headless: If headless is true Selenium will be invisible
#         :return:
#         """
#         try:
#             os.mkdir(self.pinyin_pages_directory)
#         except FileExistsError:
#             pass
#         filenames_to_convert = [f for f in os.listdir(self.compacted_pages_directory) if
#                                 isfile(join(self.compacted_pages_directory, f))]
#
#
#         for filename_to_convert in filenames_to_convert:
#             if os.path.exists(self.pinyin_pages_directory + "\\" + filename_to_convert):
#                 print('getPinyin() already done')
#             else:
#                 chrome_options = webdriver.ChromeOptions()
#                 chrome_options.headless = headless
#
#                 # The path required for chrome is pretty finicky
#                 # ODLTODO Make this more reliable
#                 path = str(Path(Path.cwd())) + "\\" + str(Path(self.pinyin_pages_directory))
#                 prefs = {"profile.default_content_settings.popups" : 0,
#                          "download.default_directory": path}
#
#                 # print("Download path: " + path + "\\" + self.pinyin_pages_directory)
#                 chrome_options.add_experimental_option("prefs", prefs)
#
#                 url = 'https://www.purpleculture.net/chinese-pinyin-converter/'
#                 driver = webdriver.Chrome(chrome_options=chrome_options,
#                                           executable_path=str(os.getcwd() + "\\" + 'chromedriver.exe'))
#                 driver.get(url)
#                 driver.maximize_window()
#                 # Grabs the definition part of the screen
#                 file_tab = driver.find_element_by_xpath('//*[@id="columnCenter"]/div[4]/div[1]/ul/li[2]/a')
#                 file_tab.click()
#                 upload_box = driver.find_element_by_id('txtfile')
#                 upload_box.send_keys(os.getcwd() + "\\" + self.compacted_pages_directory + "\\"
#                                      + filename_to_convert)
#                 convert_button = driver.find_element_by_xpath("//*[@id='fileuploadform']/div[2]/div/button[1]")
#
#                 # Scroll to this element so ads are not covering it
#                 desired_y = (convert_button.size['height'] / 2) + convert_button.location['y']
#                 current_y = (driver.execute_script('return window.innerHeight') / 2) + driver.execute_script(
#                     'return window.pageYOffset')
#                 scroll_y_by = desired_y - current_y
#                 driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
#
#                 convert_button.click()
#
#                 # Wait until file is in downloads file. Times out after 15 seconds
#                 for i in range(30):
#                     if os.path.exists(self.pinyin_pages_directory + "\\" + filename_to_convert):
#                         break
#                     time.sleep(0.5)
#                     if i == 29:
#                         print("getPinyin File not downloaded correctly")
#                 driver.quit()
