import sys
from PageScraper import csw_page_scraper, xyyuedu_page_scraper
from DatabaseBuilder import DatabaseBuilder, dictionary_maintainer
import datetime


def load_database(database_filename):

    return 0
    # DatabaseBuilder.init_database()
    # db_builder = DatabaseBuilder.DatabaseBuilder("pages/xyyuedu/移动迷宫1·找出真相")
    # db_builder = DatabaseBuilder.DatabaseBuilder("AutoAnki.db")
    # db_builder.compact_pages()
    # db_builder.add_to_database()
    #
    # csw_page_scraper.scrape_book("https://www.99csw.com/book/8831/index.htm")
    # xyyuedu_page_scraper.scrape_book("https://m.xyyuedu.com/kehuanxs/yidongmigong1_zhaochuzhenxiang/index.html")
    # xyyuedu_page_scraper.scrape_book("https://m.xyyuedu.com/guowaizuojia/jier_buleiqiaofu/shijiansharenqi/index.html")
    #
    # dictionary_maintainer.complete_unfinished_dictionary_records()


def main():


    for arg in sys.argv:
        print(arg)
    if(len(sys.argv) > 0):
        # The first argument should be the database to load.
        # If not included, will prompt for the name, or to make a new one
        database_name = sys.argv[0]


        if(database_name.split(".")[1] == "db"):
    #         Load this database
            print("Loading database: ", database_name)
            load_database(database_name)
        else:
            database_name = input("Enter the name of the database to load ('new' for new database)")
            if(database_name.lower().strip() == "new"):
                database_name = datetime.datetime
                print("Creating new database with name: ", database_name)
                load_database(database_name)

if __name__ == "__main__":
    main()

