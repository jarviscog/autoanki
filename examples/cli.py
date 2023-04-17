# import sys
# from pathlib import Path
#
# import datetime
# import os
# # from PageScraper.PageScraper import PageScraper, is_scrapable_link
# from autoanki.autoanki import autoanki
#
# # TODO Fix this file
#
#
# def terminal_interface(database_filename:str="autoanki.db"):
#
#     print("---------------------------------")
#     print("------ Welcome to autoanki! -----")
#     print("---------------------------------")
#     print("---------Type h for help---------")
#     print("---------------------------------")
#     print("Current loaded database: " + str(database_filename))
#     print("---------------------------------")
#
#     db_manager = DatabaseManager(database_filename)
#     # Use this when testing:
#     # input_string = 'f'
#     input_string = input(">").lower()
#     while 1:
#         if input_string == 'h':
#             print("-------------Options-------------")
#             print("(P)rint list of books in the database")
#             print("(U)pdate entries in the dictionary")
#             print("(M)ake a deck")
#             print("(D)atabase status/overview")
#             print("(L)ink: Add book to database")
#             print("(F)ile: Add book to database")
#             print("(Q)uit this database")
#             print("")
#         elif input_string == 'p':
#             print("Books in database:")
#             for book in db_manager.book_list:
#                 print(book)
#         elif input_string == 'u':
#             print("Updating dictionary...")
#             db_manager.complete_unfinished_records()
#         elif input_string == 'm':
#             print("Opening deck maker...")
#             deckmaker_terminal_interface(database_filename)
#         elif input_string == 'd':
#             db_manager.print_database_status()
#         elif input_string == 'l':
#             link = input("Enter the url of the book to load:\n")
#             # TODO Load book from link
#             # TODO Current work
#             if is_scrapable_link(link):
#                 parent_directory = "media\\books"
#                 scraper = PageScraper(link, parent_directory)
#                 bookpath = scraper.scrape()
#                 # db_manager.add_book_from_directory(bookpath)
#             else:
#                 print("Page is not scrapeable. Please try another link")
#         elif input_string == 'f':
#             print("Enter the filepath of the book to load.")
#             # print("")
#             path = input()
#             # TODO Load from file
#             path = str(Path(path))
#             # db_manager.add_book_from_directory("media/books/test/")
#             db_manager.add_book_from_directory(path)
#         elif input_string == 'q':
#             print("Exiting " + database_filename + "...")
#             return 0
#
#
#         input_string = input(">").lower()
#
#
# def deckmaker_terminal_interface(database_filename:str="autoanki.db"):
#
#     print("---------------------------------")
#     print("-- Welcome to the Deck Manager! --")
#     print("---------------------------------")
#     print("---------Type h for help---------")
#     print("---------------------------------")
#     print("Current loaded database: " + str(database_filename))
#     print("---------------------------------")
#
#     deck_manager = DeckManager(database_filename)
#     while(True):
#         input_string = input(">>").lower()
#         if input_string == "h":
#             print("(L)ist the books that can be added to the deck")
#             print("(A)dd all books to the deck")
#             print("(G)enerate the deck file. ")
#             print("(Q)uit")
#         elif input_string == "l":
#             book_list = deck_manager.books_in_db
#             for book in book_list:
#                 print(" - ", book)
#         elif input_string == "a":
#             book_list = deck_manager.books_in_db
#             for book in book_list:
#                 deck_manager.add_book(book)
#             print("Added all books to deck")
#         elif input_string == "g":
#             # TODO Make deck file function
#             output_file_path = deck_manager.generate_deck_file()
#             print("Created deck file! File is in: " + output_file_path)
#         elif input_string == "q":
#             return 0
#
#
# def main():
#     # # Main will run both the flask server as well as a terminal ui
#     # server_process = Process(target=flask_server.main(), args=('',))
#     # server_process.daemon = True
#     # server_process.start()
#
#     # Check if the first argument was a database file
#     if(len(sys.argv) > 0):
#         # The first argument should be the database to load.
#         # If not included, will prompt for the name, or to make a new one
#         database_name = sys.argv[1]
#         if is_database(database_name):
#             print("Loading database: ", database_name)
#         else:
#             print("Error loading \"" + database_name + "\"")
#
#
#     while 1:
#         # Grab a valid database filename
#         while not is_database(database_name):
#             database_name = input("Enter the name of the database to load ('new' for new database): ")
#             if(database_name.lower().strip() == "new"):
#                 input_string = input("Enter name of database, or press enter: ")
#                 if input_string == None:
#                     database_name = datetime.datetime.now().strftime("auto-anki_%d-%m-%y.db")
#                 else:
#                     database_name = input_string
#                 if is_valid_database_filename(database_name):
#                     print("Creating new database` with name: " + database_name)
#                     create_autoanki_database(database_name)
#                 else:
#                     print("Sorry, that filename is not valid.")
#             else:
#                 if is_database(database_name):
#                     print("Loading database: ", database_name)
#                 else:
#                     print("Error loading \"" + database_name + "\"")
#
#         # Once a valid database has been loaded (or created), then load the terminal interface
#         terminal_interface(database_name)
#         # If the user quits, this will reset and let the user choose another database
#         database_name = ""
#         print("")
#
# if __name__ == "__main__":
#
#     main()
