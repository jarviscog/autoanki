> **Note** <br>
Massive refactoring in progress!

# AutoAnki
 Auto-Generate Anki Flashcards from a text file.
 
 Converts Chinese books from a few online libraries into flash cards for Anki, containing definitions and images
 
Additionally, AutoAnki is able to sort the cards based on the most frequently used characters in the text, as well as ignore words that have already been uploaded from a previous book.
 
AutoAnki was created to help Chinese learners get into more advanced texts. It can be hard transitioning from graded readers to full books, and this tool was designed to help.

## Usage

AutoAnki scrapes definitions and pinyin from two websites using Selenium for Chrome.
Check your version of Chrome, and put the same version driver in the same directory as main.
Drivers can be found here ---> https://chromedriver.chromium.org/downloads
Install requirements.txt and run main.py

![book on website](https://github.com/timmy6figures/AutoAnki/blob/main/bookex.PNG?raw=true)

## Files

See `code_outline.md` for more info on the files and how they are used.


# Limitations

- Only mandarin texts have been tested so far, This tool probbably works for traditional characters, but it has not been tested.
- If used too much, websites will block traffic coming from your computer. To fix this proxies will be needed, but this feature has not been added yet.

 
