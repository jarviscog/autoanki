Current roadmap for the project.
- [x] Means completed
- [ ] Means an unfinished item
- [?] Means a potential feature. Decide if needed, and act accordingly

## v1.2.3

- [x] Remove the use of .db files. This feature turns out to not be that useful
- [x] Remove loading bar. Show timing info in logs
- [x] Add more unit tests


Features:
- [ ] Tone Colors
- [ ] Handwritten characters
- [ ] Play audio
- [ ] Filters
    - Verify card filters work
    - Filter by most common Xk words
- [ ] Spanish support
    - [ ] Dictionary
    - [ ] Card settings
- [ ] Split settings setter into multiple functions. That function is too large

Performance:
- [ ] Run performance testing on a range of input files
- [ ] Multithreading to improve dict lookup speed
- [ ] Move dictionary to a MySQL database
    - Create a bunch of tables for each language's features. 
    Then, when a list of words come in inner join all the requested features into one table

Debugging:
- [ ] Store logs as file
- [ ] Find a way to check cards for junk data (Fix Q, P from airplanes)
- [ ] Write unit tests for settings

- [ ] Add number of cards added to deck to logs

Other decks:
- [ ] More books
- [ ] HSK Decks

## v1.2.2
- [x] Add aa version number to logs

## v1.2.1 (Mandarin+ Update)
- Backend
- [x] Dictionary use dict instead of list
- [x] Address TODOs
- [x] Confirm pass in dictionary works
- [x] Add back support for multi-file book
- [x] Faster book scraping
- [x] Finish part of speech analysis
- [x] Don't run db populate based on settings

- Database
- [x] Dedicated Chinese database
- [x] rename cantonese column to juytping
- [x] Zhuyin
- [x] Audio

- Cards
- [x] Filter by HSK level
- [x] Filter by word frequency

- Imports/Exports
- [x] Import txt files (Pleco)
- [x] Import epub files
- [x] Import Pdf files
- [x] Export as csv

## v1.2.0
- First website-ready version
- Backend
- [x] Ability to omit database name
- [x] Remove BookCleaner and merge into Tokenizer/DatabaseManager
- [x] Issues installing libraries
- [x] Add ability to add book from string
- [x] Add automated tests
- [x] Convert database magager to abstract class to prepare for multi-language
- [x] Add option to use custom dictionary
- [x] Add language setting for AutoAnki constructor
- [x] Faster load-up times

- Improved Cards
- [x] Add part-of-speech to card

- Docs/Non-code
- [x] Logo/Branding
- [x] Update README

## v1.1.91
- [x] Fix nested relative paths in BookCleaner
- [x] Remove superfluous slashes from CE-DICT definitions
- [x] Remove logs from libraries
- [x] confirm requirements install correctly
- [x] Add documentation

## v1.1.9
- Filtering/Defining
- [x] Seperate Chinese tokenizer from DatabaseManager
- [x] Improve table for part-of-speech
- [x] Fix relative imports in pip version
- [x] Traditional word should exclusively replace only different words
- [x] Filter non-ascii latin character set (Don't filter T恤)
- [x] Remove Chinese-spesific parts from AutoAnki.py
- [x] complete_unfinished_definitions() should only be run once
- [x] Fix word count after dictionary word-split

- [x] [Better Word Frequency Data](https://lingua.mtsu.edu/chinese-computing/statistics/char/list.php?Which=MO)
- Card filters
- [x] Filter by word frequency

## v1.1.8
- Dictionary
- [x] Better Dictionary lookups (80%> hit-rate)
    - [x] Filter numbers and number-subject tokens
    - [x] Missed Dictionary lookups < 3 characters will return split definitions
    - [x] Same character repeated twice/thrice

- [x] Add tags to cards
- [x] Add `--force` option to deck cleaner
- [x] Documentation for how Dictionaries work
- Batch One Decks!

## v1.1.7
- Card settings
- [x] Add formatting settings to cards
- [x] More customization for card apperance
- [x] Filter Grammar from database better

## v1.1.5
- [x] Fix Images on Pypi
- [x] Logging level set by autoanki
- [x] Better formatted dictionary lookups
- [x] Faster Dictionary Lookups

## v1.1.0
- [x] Verify all components working
- [x] Format logging output
- [x] Use local dictionary for word lookups
- [x] Clean input of numbers, whitespace, etc.
- [x] Updated README.md

