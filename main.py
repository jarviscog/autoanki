from PageScraper import csw_page_scraper, xyyuedu_page_scraper
from DatabaseBuilder import DatabaseBuilder, dictionary_maintainer

if __name__ == "__main__":

    # DatabaseBuilder.init_database()

    db_builder = DatabaseBuilder.DatabaseBuilder("pages/xyyuedu/移动迷宫1·找出真相")
    db_builder.compact_pages()
    db_builder.add_to_database()

    csw_page_scraper.scrape_book("https://www.99csw.com/book/8831/index.htm")
    xyyuedu_page_scraper.scrape_book("https://m.xyyuedu.com/kehuanxs/yidongmigong1_zhaochuzhenxiang/index.html")
    xyyuedu_page_scraper.scrape_book("https://m.xyyuedu.com/guowaizuojia/jier_buleiqiaofu/shijiansharenqi/index.html")

    dictionary_maintainer.complete_unfinished_dictionary_records()
