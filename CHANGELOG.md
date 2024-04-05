# Changelog

## v1.0.9 (05/05/2023)

### Bugfix
- Fixed setup.cfg bad imports

## v1.0.7 (05/05/2023)

### Bugfix
- Fixed imports
- Added missing sql files to package

## v1.0.5 (17/04/2023)

### Feature

- Added LICENCE

## v1.0.0 (17/04/2023)

- First release of `autoanki`

## v1.1.0 (04/05/2024)

- Fixed bugs
- Removed legacy files
- Changed dictionary to use local file, rather than internet lookups
- Formatted logging output
- Updated README.md
- Cleaned input to remove punctuation


## v1.1.5 (DD/MM/2024)
- Updated README.md
- Moved DeckManager out of __init__.py
- If the user included .apkg at the end, ignore it
- Logger for each module is now set by AutoAnki
- Fixed images displaying on Pypi
- Made Database mandager functions more verbose
- Now uses internal CC-CEDICT file
- Faster dictionary lookups by using internal state
- Better dictionary formatting
