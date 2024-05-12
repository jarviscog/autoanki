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
- Backend
- [ ] Add option to use custom dictionary
- [ ] Convert database magager to abstract class to prepare for multi-language
- [ ] Improve dictionaries
- [ ] Address TODOs
- [ ] Remove BookCleaner and merge into Tokenizer/DatabaseManager
- [ ] Issues installing:
    - chinese-converter
    - wordfreq
    - pinyin
    - genanki
- [ ] Ability to omit database name
- [x] Add ability to add book from string
- [ ] Find tools to do profiling on speed

- Improved Cards
- [ ] Add part-of-speech to card
- [ ] Option to include English -> Chinese cards
- [ ] Add minimum number of repititions before getting added to the deck
- [ ] Option to add book name as a tag
- [?] Output books as subdecks

- Docs/Non-code
- [ ] Logo/Branding

## v1.2.1

- [ ] Filter by HSK level
- [ ] Faster book scraping
- [ ] Update README

## Potential New Features

- AutoAnki
- [?] Progress bars for cleaner output
- [?] Add terminal options back in/Update README

- Debug/Testing
- [?] Delete database definitions
- [?] Add automated tests

- Cards
- [?] Add audio to cards
- [?] Add images to cards
- [?] Embed links to online dictionary in cards

- Features
- [?] Add ability to use epub files from kindle
- [?] Chinese Idioms?
- [?] Song lyrics?
- [?] English word + definition style cards?
- [?] Multiple supported languages?
- [?] Show word from the context in which it showed up

- [?] Grammatical patterns?
- [?] 成语?
- [?] Estimate HSK level of word from sub-words

