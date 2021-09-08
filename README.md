# AutoAnki
 Auto-Generate Anki Flashcards from a text file.
 
 Converts a text file containing Chinese characters into flash cards for Anki, containing definitions and images
 
 Additionally, AutoAnki is able to sort the cards based on the most frequently used characters in the text, as well as ignore words that have already been uploded in a previous file.
 
AutoAnki was created to help Chinese learners get into more advanced texts.
 
# Details

AutoAnki scrapes definitions and pinyin from two websites using selenium for chrome.
Check your version of chrome, and put the same version driver in the same directory as main.
Drivers can be found here ---> https://chromedriver.chromium.org/downloads

# Limitations

- Some of the websites used have a limit to the file size uploded. Currently AutoAnki only supports files up to 300kb in size. Some automatic splitting and re-joining of files are planned.
- Only mandarin texts have been tested so far, support for Cantonese is a possibility, but not a priority.
- If used too much, websites will block traffic coming from your computer. To fix this use a proxy

 
