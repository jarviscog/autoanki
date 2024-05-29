Current roadmap for the project. 
- [x] Means completed
- [ ] Means an unfinished item
- [?] Means a potential feature. Decide if needed, and act accordingly

## v1.1.0
- [x] Verify all components working
- [x] Format logging output
- [x] Use local dictionary for word lookups
- [x] Clean input of numbers, whitespace, etc.
- [x] Updated README.md

## v1.1.5
- [x] Fix Images on Pypi
- [x] Logging level set by autoanki
- [x] Better formatted dictionary lookups
- [x] Faster Dictionary Lookups

## v1.1.7
- Card settings
- [x] Add formatting settings to cards
- [x] More customization for card apperance
- [x] Filter Grammar from database better

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

## v1.1.91
- [x] Fix nested relative paths in BookCleaner
- [x] Remove superfluous slashes from CE-DICT definitions
- [x] Remove logs from libraries
- [x] confirm requirements install correctly
- [x] Add documentation

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

## v1.2.3 (Spanish Update)
- [ ] Add more unit tests
- [ ] Dictionary
- [ ] Database Manager
- [ ] Deck Manager

## Planned features

- [ ] Show word from the context in which it showed up
- [ ] Fill HSK level for all sub-chars of available chars
- [ ] Colored characters
- [ ] Filter by most common Xk words

- [ ] Store logs as file

- Card types
- [ ] Cloze deletion card
- [ ] Reverse card type

- [ ] Batch 2: Add HSK decks
- [ ] Add more tests
- [ ] Restructure so each file can be passed to database_manager and still get added to the same book
- [ ] Handwritten characters
- [ ] Other card types
- [ ] Add images to cards
- [ ] Import epub files from kindle
- [ ] Exapmle sentances

## Potential New Features
- AutoAnki
- [?] Progress bars for cleaner output
- [?] Add terminal options back in
- [?] Output books as subdecks
- [?] Option to add book name as a tag
- [?] Add minimum number of repititions before getting added to the deck
Process/
- [?] Auto documentation using 'Read the Docs'
- [?] Automatic profiling system to see performance
- [?] Outsource faster running times for process

- Cards
- [?] Embed links to online dictionary (pleco) in cards

- Features
- [?] Chinese Idioms?
- [?] Song lyrics?
- [?] English word + definition style cards?

- [?] Grammatical patterns?
- [?] 成语?

