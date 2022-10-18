import time

import requests
from bs4 import BeautifulSoup
import os
# Scrapes books from the website 99csw.com
# Made by Jarvis Coghlin

def scrape_book(book_link):

    main_page = requests.get(book_link).content
    chapters = []
    page = "https://www.99csw.com"
    main_page_soup = BeautifulSoup(main_page, "html.parser")

    book_title = main_page_soup.find(id="book_info").find('h2').contents[0]

    new_directory_path = os.getcwd() + "\\" + "pages\\99csw" + "\\" + book_title
    # print(type(new_directory_path))
    try:
        os.mkdir(new_directory_path)
    except FileExistsError:
        pass

    # Get the directory tag, and find all links within:
    links = main_page_soup.find(id="dir").find_all('a')
    for link in links:

        # print(link.contents[0])
        chapter_page = requests.get("https://www.99csw.com" + link['href']).content
        current_chapter_page_soup = BeautifulSoup(chapter_page, "html.parser")
        content = current_chapter_page_soup.find(id='content').children
        for i in range(19):
            next(content)
        # Visible text is separated by junk divs probably to stop scraping
        # print(type(content))
        try:
            while True:
                print(next(content))
        except:
            print("Chapter done")

            # for con in content:
            # print(con)

        time.sleep(1)


def save_text_from_chapter(link):
    print("Get text from chapter")
    # Parse
    # Save file

