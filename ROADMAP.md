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

## v1.2.0
- Speed:
- [ ] Faster book scraping

- [ ] Filter by HSK level

- [ ] Fix nested relative paths in BookCleaner
- [ ] Option to add book name as a tag
- [ ] Add part-of-speech to card

- [ ] Logo/Branding
- Batch Two Decks?

## Potential New Features

- [ ] Progress bars for cleaner output
- [ ] Output books as subdecks
- [ ] Add automated tests

- Debug Tools
- [ ] Delete database definitions

- [?] Add audio to cards
- [?] Add images to cards
- [?] Embed links to online dictionary in cards?

- [?] Multiple supported languages?
- [?] English word + definition style cards?
- [?] Grammatical patterns?
- [?] Estimate HSK level of word from sub-words
- [?] 成语?
- [?] Chinese Idioms?
- [?] Song lyrics?
- [?] Add terminal options back in

