import sys
from PageScraper import csw_page_scraper, xyyuedu_page_scraper
from DatabaseManager.DatabaseManager import DatabaseManager, create_autoanki_database, is_database
import datetime
import pyfiglet
import os

def load_database(database_filename):

    # db_manager.compact_pages()
    # db_manager.add_to_database()
    #
    # csw_page_scraper.scrape_book("https://www.99csw.com/book/8831/index.htm")
    # xyyuedu_page_scraper.scrape_book("https://m.xyyuedu.com/kehuanxs/yidongmigong1_zhaochuzhenxiang/index.html")
    # xyyuedu_page_scraper.scrape_book("https://m.xyyuedu.com/guowaizuojia/jier_buleiqiaofu/shijiansharenqi/index.html")
    #
    # dictionary_maintainer.complete_unfinished_dictionary_records()
    return 0

def terminal_interface(database_filename):

    # TODO Use pyfiglet to make the UI nice
    print("---------------------------------")
    print("------ Welcome to AutoAnki! -----")
    print("---------------------------------")
    print("---------Type h for help---------")
    print("---------------------------------")
    print("Current loaded database: " + str(database_filename))
    print("---------------------------------")

    db_manager = DatabaseManager(database_filename)
    # Use this when testing
    input_string = ''

    while 1:

        if input_string == 'h':
            print("-------------Options-------------")
            print("(P)rint list of books in the database")
            print("(U)pdate entries in the dictionary")
            print("(M)ake a deck")
            print("(D)atabase status/overview")
            print("(L)ink: Add book to database")
            print("(F)ile: Add book to database")
            print("(Q)uit this database")
            print("")
        elif input_string == 'p':
            print("Books in database:")
            for book in db_manager.book_list:
                print(book)
        elif input_string == 'u':
            print("Updating dictionary...")
            db_manager.complete_unfinished_dictionary_records()
        elif input_string == 'm':
            print("Opening deck maker...")
            # TODO Make deck maker
        elif input_string == 'd':
            db_manager.print_database_status()
        elif input_string == 'l':
            link = input("Enter the url of the book to load")
            # TODO Load book from link
            db_manager.add_book_from_link(link)
        elif input_string == 'f':
            link = input("Enter the url of the book to load")
            # TODO Load from file
        elif input_string == 'q':
            print("Exiting " + database_filename + "...")
            return 0

        input_string = input(">").lower()


def main():

    # Check if the first argument was a database file
    if(len(sys.argv) > 0):
        # The first argument should be the database to load.
        # If not included, will prompt for the name, or to make a new one
        database_name = sys.argv[1]
        if is_database(database_name):
            print("Loading database: ", database_name)
        else:
            print("Error loading \"" + database_name + "\"")


    while 1:
        # Grab a valid database filename
        while not is_database(database_name):
            database_name = input("Enter the name of the database to load ('new' for new database): ")
            if(database_name.lower().strip() == "new"):
                input_string = input("Enter name of database, or press enter: ")
                if input_string == None:
                    database_name = datetime.datetime.now().strftime("AutoAnki_%d-%m-%y.db")
                else:
                    database_name = input_string
                print("Creating new database with name: " + database_name)
                create_autoanki_database(database_name)
            else:
                if is_database(database_name):
                    print("Loading database: ", database_name)
                else:
                    print("Error loading \"" + database_name + "\"")

        # Once a valid database has been loaded (or created), then load the terminal interface
        terminal_interface(database_name)
        # If the user quits, this will reset and loop
        database_name = ""
        print("")


if __name__ == "__main__":
    main()