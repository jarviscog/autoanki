# Changelog
- All notable changes to this project will be documented here

## v1.1.9 (2024/05/15)
- Seperated text tokenizer into new class (with abstract class)
- Removed legacy code from BookCleaner
- Added `chinese-converter` to requirements
- Fix relative imports in pip version, and included cedict_ts.u8
- Now exclusively replaces only different characters
- Added ablility to use user-specified dictionary
- Removed Chinese-spesific code from AutoAnki.py
- Added word frequency data to database
- Added ability to filter cards based on frequency

## v1.1.8 (2024/05/11)
- Added `autoanki` tag to all cards generated
- Added smarter dictionary lookups, including removing numbers, same character twice (宝宝), and splitting some words
- Added `force` option to skip confirming cleaning large numbers of files
- Added documentation for Dictionary
- Reordered CHANGELOG.md

## v1.1.7 (2023/05/07)
- Added pinyin with symbols, instead of numbers
- Added part of speech. (Noun, verb, etc.)
- Added ability to add book from directory
- Traditional books now format correctly in the database
- Improved Puncuation filtering

## v1.1.6 (2023/05/05)
- Removed unnecessary logging output
- Set multiple definitions on newlines

## v1.1.5 (2023/05/05)
- Updated README.md
- Moved DeckManager out of __init__.py
- If the user included .apkg at the end, ignore it
- Logger for each module is now set by AutoAnki
- Fixed images displaying on Pypi
- Made Database mandager functions more verbose
- Now uses internal CC-CEDICT file
- Faster dictionary lookups by using internal state
- Better dictionary formatting

## v1.1.0 (2023/05/05)
- Fixed bugs
- Removed legacy files
- Changed dictionary to use local file, rather than internet lookups
- Formatted logging output
- Updated README.md
- Cleaned input to remove punctuation

## v1.0.9 (2023/05/05)
- Fixed setup.cfg bad imports

## v1.0.7 (2023/05/05)
- Fixed imports
- Added missing sql files to package

## v1.0.5 (2023/04/17)
- Added LICENCE

## v1.0.0 (2023/04/17)
- First stable release of `autoanki`
