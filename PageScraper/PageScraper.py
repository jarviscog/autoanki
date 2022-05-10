from PageScraper import xyyuedu_page_scraper, csw_page_scraper

# TODO Make a more general page scraper. The current scrapers could extend this new class

def is_scrapable_link(url):
    """
    Makes sure the url is a valid url, and from a page that is scrapeable
    :return: 1 if true, 0 if false
    """
    # TODO is_scrapable_link()
    return 1


class PageScraper:

    def __init__(self, url_to_scrape: str, parent_directory):
        """
        A class to scrape books of of spesific sites, and store them as text files in a directory
        :param url_to_scrape: The url of the website where the page is located. This should not be a chapter,
        but the index
        :param destination_directory: The parent of the location where the scraped book will be stored. Each chapter
        of the book will be a different text file
        """
        self.url = url_to_scrape

        # TODO Check if user has write permission in this directory (This is really extra. DON'T DO THIS FOR V1 JARVIS)
        # TODO Check if book has already been scraped/directory exists (Maybe do this one)
        # print("parent: ", parent_directory)
        self.parent_directory = parent_directory

        self.domain = ""

    def scrape(self):
        """

        :return: Returns the filepath of the book that was scraped. This is where all of the chapter .txt files have been downloaded to.
        """

        if not is_scrapable_link(self.url):
            print("Link is not valid. Please change the url to a valid link")
        else:
            print("Scraping page...")

            if self.domain == "xyyuedu":
                print("Scraping an xyyuedu book...")
                # TODO xyyuedu scaper
                xyyuedu_page_scraper.scrape_book(self.url, self.parent_directory)
            elif self.domain == "99csw":
                print("Scraping an 99csw book...")
                # TODO 99csw scraper
            else:
                print("Currently there is not a scraper for this site.")
                return 0

        bookpath = "pages/Book1"
        return bookpath

    @property
    def domain(self):
        split_url = self.url.split(".")
        domain_string = split_url[1]
        return domain_string

    @domain.setter
    def book_list(self, value):
        self.domain = value

    @domain.setter
    def domain(self, value):
        self._domain = value
