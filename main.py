import sys
from pathlib import Path

from PageScraper import csw_page_scraper, xyyuedu_page_scraper
from DatabaseManager.DatabaseManager import DatabaseManager, create_autoanki_database, is_database, is_valid_database_filename
import datetime
import flask_server
from multiprocessing import Process
import pyfiglet
import os
from PageScraper.PageScraper import PageScraper, is_scrapable_link
from DeckMaker.DeckMaker import DeckMaker

# csw_page_scraper.scrape_book("https://www.99csw.com/book/8831/index.htm")
# xyyuedu_page_scraper.scrape_book("https://m.xyyuedu.com/kehuanxs/yidongmigong1_zhaochuzhenxiang/index.html")
# xyyuedu_page_scraper.scrape_book("https://m.xyyuedu.com/guowaizuojia/jier_buleiqiaofu/shijiansharenqi/index.html")

def terminal_interface(database_filename:str="AutoAnki.db"):

    # TODO Use pyfiglet or similar to make the UI nice
    print("---------------------------------")
    print("------ Welcome to AutoAnki! -----")
    print("---------------------------------")
    print("---------Type h for help---------")
    print("---------------------------------")
    print("Current loaded database: " + str(database_filename))
    print("---------------------------------")

    db_manager = DatabaseManager(database_filename)
    # Use this when testing:
    # input_string = 'f'
    input_string = input(">").lower()
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
            link = input("Enter the url of the book to load:\n")
            # TODO Load book from link
            # TODO Current work
            if is_scrapable_link(link):
                parent_directory = "media\books"
                scraper = PageScraper(link, parent_directory)
                bookpath = scraper.scrape()
                db_manager.add_book_from_directory(bookpath)
            else:
                print("Page is not scrapeable. Please try another link")
        elif input_string == 'f':
            print("Enter the filepath of the book to load.")
            # print("")
            path = input()
            # TODO Load from file
            path = str(Path(path))
            db_manager.add_book_from_directory("media/books/test/")
        elif input_string == 'q':
            print("Exiting " + database_filename + "...")
            return 0


        input_string = input(">").lower()

def deckmaker_terminal_interface(database_filename:str="AutoAnki.db"):
    print("---------------------------------")
    print("--- Welcome to the Deck Maker! --")
    print("---------------------------------")
    print("---------Type h for help---------")
    print("---------------------------------")
    print("Current loaded database: " + str(database_filename))
    print("---------------------------------")

    deckmaker = DeckMaker(database_filename)
    manager = DatabaseManager(database_filename)
    while(True):
        input_string = input(">>").lower()
        if input_string == "h":
            print("(L)ist the books that can be added to the deck")
            print("(A)dd all books to the deck")
            print("(G)enerate the deck file. ")
        elif input_string == "l":
            book_list = manager.book_list
            for book in book_list:
                print(book)
        elif input_string == "a":
            book_list = manager.book_list
            for book in book_list:
                deckmaker.add_book(book)
            print("Added all books to deck")
        elif input_string == "g":
            # TODO Make deck file
            output_file_path = deckmaker.generate_deck_file()
            print("Created deck file! File is in: " + output_file_path)





def main():
    # # Main will run both the flask server as well as a terminal ui
    # server_process = Process(target=flask_server.main(), args=('',))
    # server_process.daemon = True
    # server_process.start()

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
                if is_valid_database_filename(database_name):
                    print("Creating new database` with name: " + database_name)
                    create_autoanki_database(database_name)
                else:
                    print("Sorry, that filename is not valid.")
            else:
                if is_database(database_name):
                    print("Loading database: ", database_name)
                else:
                    print("Error loading \"" + database_name + "\"")

        # Once a valid database has been loaded (or created), then load the terminal interface
        terminal_interface(database_name)
        # If the user quits, this will reset and let the user choose another database
        database_name = ""
        print("")

if __name__ == "__main__":

    main()