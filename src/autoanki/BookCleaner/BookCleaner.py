import logging
import os

# TODO: I think that the entire book cleaner file is not needed. 
#   Words should not be written back to a file. This is slow
CLEANED_FILES_DIRECTORY = 'cleaned_files'
CLEANED_FILES_SUFFIX = '_cleaned'
# Sentences That should not be added to the completed file.
GARBAGE_SENTENCES = ['',
                     "",
                     ".",
                     "。",
                     "\n"]


class BookCleaner:

    def __init__(self, debug_level, force=False):
        """ Internal tool used to sanatize input
        Use `clean(bookpath)` to sanatize files and remove junk data
        Args:
            `force`: Ignore confirmations on if you want to clean >50 files
        """
        self.logger = logging.getLogger('autoanki.bookcleaner')
        self.logger.setLevel(debug_level)
        self.file_list = []
        self.bookpath = ""
        self.force = force

    def clean(self, bookpath: str) -> None | list[str]:
        """
        Cleans the files contained in the bookpath. If bookpath is a single file, clean it.
        Args: 
            `bookpath: filepath of files to be cleaned`
        Return: 
            `str: list of cleaned file(s)`
        """
        if not os.path.exists(bookpath):
            self.logger.warning("Cannot find path [" + str(bookpath) + "]")
            return None
        self.logger.info("Bookpath: " + bookpath)

        # If the bookpath is a single file, clean and return it
        if os.path.isfile(bookpath):
            cleaned_files = [self._clean_file(bookpath, cleaned_files_root=None)]
            return cleaned_files
        else:
            dirty_files = []
            for root, dirs, files in os.walk(bookpath):
                for file in files:
                    # Only clean files that are not in cleaned_files directory
                    in_cleaned = str(root).find(CLEANED_FILES_DIRECTORY) != -1
                    if not in_cleaned:
                        if '.txt' in file:
                            dirty_files.append(os.path.join(root, file))

            # Check this cleaning won't be mean to the CPU
            if len(dirty_files) > 50 and not self.force:
                yn = input("Over 50 files. Are you sure you want to convert this many files? (Y/N)")
                if yn.lower() != 'y':
                    return None

        # Now we have a list of files to convert in a list
        cleaned_files = []

        # Create directory for files
        cleaned_files_root = os.path.join(bookpath, CLEANED_FILES_DIRECTORY)
        if not os.path.exists(cleaned_files_root):
            os.mkdir(cleaned_files_root)

        for file in dirty_files:
            cleaned_filepath = self._clean_file(file, cleaned_files_root=cleaned_files_root)
            if cleaned_filepath:
                cleaned_files.append(cleaned_filepath)

        return cleaned_files

    def _clean_file(self, filepath: str, cleaned_files_root: str):
        """
        Takes a txt file and cleans it up, filtering junk and putting every sentence on a new line
        Args:
            `filepath`: The txt file to clean
            `cleaned_files_root`: The root
        """

        # TODO: This will not work for books with nested files that share the same name
        filename = os.path.basename(filepath)
        new_filepath = os.path.join(cleaned_files_root, filename)
        self.logger.debug("Filepath:     " + filepath)
        self.logger.debug("New filepath: " + new_filepath)

        # Clean page file of characters that may cause issues.
        page_file = open(filepath, encoding='utf-8')
        try: 
            page_sentences = page_file.read().split("。")
        except:
            self.logger.error(f"Critical error cleaning file: [{filepath}]")
            return
        cleaned_file = open(new_filepath, "w", encoding='utf-8')

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
                .strip("'")\
                .strip("'")
            if page_sentence not in GARBAGE_SENTENCES:
                cleaned_file.write(page_sentence + "。" + "\n")

        return new_filepath

