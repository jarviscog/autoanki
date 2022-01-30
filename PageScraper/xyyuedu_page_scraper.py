import time
import requests
from bs4 import BeautifulSoup
import unicodedata
import os
import re
# Scrapes books from the website xyyuedu.com
# Made by Jarvis Coghlin


# TODO Fix the multiple bugs in this function
def scrape_book(book_link):
    main_page = requests.get(book_link).content
    chapters = []
    page = "https://www.99csw.com"

    main_page_soup = BeautifulSoup(main_page, "html.parser")

    book_title = main_page_soup.find('h1', class_='htitle111').contents[0].contents[0]
    clean_title = unicodedata.normalize("NFKC", book_title)
    new_directory_path = os.getcwd() + "\\" + "pages\\xyyuedu" + "\\" + clean_title
    try:
        os.mkdir(new_directory_path)
    except FileExistsError:
        pass
    links = []
    # Get the directory tag, and find all links within:
    links = main_page_soup.find(class_="all_chapter").find_all('a')
    for link in links:
        print(link)
        # print(link.contents[0])
        try:
            scrape_chapter_page(link, new_directory_path)
        except Exception as e:
            print("Error downloading: " + link.contents[0])
            print(str(e))
        print("")
        time.sleep(1)

def scrape_chapter_page(link, filepath):

    chapter_page = requests.get("https://m.xyyuedu.com" + link['href'],
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'},

    )
    current_chapter_page_soup = BeautifulSoup(chapter_page.content)
    text = str(current_chapter_page_soup.findAll(text=True))
    print(text)
    # print(len(chapter_page.text))
    # print(chapter_page.text)
    # print(current_chapter_page_soup)
    try:
        content = current_chapter_page_soup.find(id='onearcxsbd').text
    except AttributeError:
        try:
            content = current_chapter_page_soup.find(id='nr1').getText()
        except Exception as e:
            # print(current_chapter_page_soup)
            print(e)
    # TODO OTHER ID
    # Scrub all junk characters from content
    # content = re.sub("[\u3000\t\r\n\ax03]", "", content)
    chapter_title = current_chapter_page_soup.find(id='arcxs_title').find('h1').getText()
    # print(chapter_title)
    # print(content)
    # print(len(content))
    # print(type(content))
    content_sentence_list = content.split("。")
    file = open(filepath+ "\\" + chapter_title + ".txt", 'w', encoding='utf-8')
    for sentence in content_sentence_list:
        file.write(sentence + "\n")