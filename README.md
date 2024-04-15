> **❗️** <br>
Pull requests welcome! If you think you can improve AA in any way, open a PR!

# autoanki
Tool for generating Anki flashcards to learn Chinese.

<img src="https://github.com/timmy6figures/autoanki/blob/main/media/images/example.jpg?raw=true" alt="Text to Anki" width="80%"/>

## Motivation

When learning Chinese, some common advice is to learn the top X most common words.
This is good advice, as you can get pretty far with this, however it's [not perfect](https://en.wikipedia.org/wiki/Zipf%27s_law#/media/File:Zipf's_law_on_War_and_Peace.png).

For example, Harry Potter. This book will have normal distribution for most words, however there will be a heavy emphasis on a specialized subset of words such as Wand, Robe, Wizard, Broomstick etc. These words will show up a lot more than they would otherwise.

The intention of this package was to allow Chinese learners to move from beginner books to more advanced material. I found there was a gap in knowledge going from beginner learning books (where there is little specalized terminology), to teen novels, where each novel will generally have its own specialized terminology, making the transition tedious. This is solved by automatically making Anki decks that have this specialized terminology, so that you are able to memorize these words while continuing to make progress

With autoanki, you selectively add words to an Anki file to continue progressing with your lanuage learning skills.

## Usage

autoanki is both a library and a command-line tool.

To get started, run 
```pip install autoanki```
This should install all the requirements. Then, in a Python file, do ```from autoanki import AutoAnki```

To get started, first, create a database for autoanki to use 
```    
db_path = "AutoAnki.db"
if not AutoAnki.is_database(db_path):
    AutoAnki.create_database(db_path)
```
Then create an instance of autoanki using the database
```
aa = AutoAnki(db_path)
```
Add whatever books you want in your deck. These can be a single file, or a folder
```
bookpath = 'short-story.txt'
aa.add_book(bookpath, 'My first book🍎')
```
Once all of your books are added, the definitions need to be found, and then you can create a deck!
```
aa.complete_unfinished_definitions()
aa.create_deck("AutoAnki Deck", "output")
```
This will automatically have the .apkg extension, which Anki uses. 
Import this file into Anki, and you're all set.

#### Other commands
If you want to see the status of the database, use:
```
aa.print_database_info()
```
If you would like to create and use your own dictionary, you can pass it in when you 
```
aa = AutoAnki(db_path, dictionary=CustomDictionary())
```
This dictionary must implement functions from the abstract class `autoanki/Dictionary.py`

Some settings can be set regarding how cards will be formatted, and what will be shown. They can be seen here:
```
aa.deck_settings(
include_traditional=True,
include_part_of_speech=True,
word_frequency_filter=1e-05 # Float between 0 and 1. Filters using this library: https://pypi.org/project/wordfreq/
)
```

## How it works
AutoAnki interfaces has 4 components on the back end:
1. BookCleaner: Cleans the input coming in from files that the user supplies 
2. DatabaseManager: Takes the cleaned input and puts it into the database
3. Dictionary: Finds definitions for words in the database
4. DeckManager: Creates Decks

### Dictionary
This is an abstract class that can be implemented with the following methods
- `__init__(debug_level)`
- `find_word(word)` - Returns None, or a list of paramaters that match the input of DatabaseManager.update_definition()
- `size()` - Number of entries in the dictionary

There is one dictionary included as the default: an endpoint to [CC-CEDICT](https://www.mdbg.net/chinese/dictionary?page=cedict). 
I have local versions of other dictionaries with copyrighted data, which I can not upload.

### Database
There are 3 different types of tables in the DB:
- `dictionary` contains a information about each word, including the pinyin, traditional characters, and a definition
- `book_list` contains the book name, table name, and language for each book added
- `book` contains the book table id, dictionary word id, and the number of appearances for each word in the book
  
<img src="https://github.com/timmy6figures/autoanki/blob/main/media/images/dictionary-table.jpg?raw=true" alt="Dictionary table" width="60%"/>
<img src="https://github.com/timmy6figures/autoanki/blob/main/media/images/book_list_table.jpg?raw=true" alt="Book list table" width="50%"/>
<img src="https://github.com/timmy6figures/autoanki/blob/main/media/images/book_table.jpg?raw=true" alt="Book table" width="40%"/>

## Planned features
- See ROADMAP.md

## Other Info

If you would like to get involved, or learn more information, reading Anki documentation is really important, especially the [Getting Started](https://docs.ankiweb.net/getting-started.html)

To get definitions, this autoanki uses the [CC-CEDICT]() under the creative commons licence. 

