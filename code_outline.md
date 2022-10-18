# Structure

AutoAnki interfaces has 2 components on the back end. 
1. BookCleaner cleans the input coming in from files that the user supplies 
2. DatabaseManager takes the cleaned input and puts it into the database
3. DeckManager takes information from the user and database, and makes an Anki deck 
out of it


## Database:

There are 3 different types of tables in the DB, 
1. dictionary, which holds all of 
the definitions and other information 
2. book_list, which holds the titles of the books in the database 
3. book, based off of the name of the book, and holds the words in the book to find in the dictionary


### dictionary:
- word_id
- word
- word_traditional
- word_type (noun, verb, etc.)
- pinyin
- pinyin_numbers
- number_of_strokes
- sub_components
- frequency
- hsk_level
- top_level
- audio_path
- image_path
- definition


### book_list:
- book_name
- book_table_name
- language


### book_example
 - id
 - word
 - number_of_appearances

## Tasks

### Deck Maker
1. Take book name(s) as input 
2. Get desired tables from the book_list table 
3. Read the table for each book in the database. 
4. For each word, read from the definitions table to get all other information 
5. Create notes for every word 
6. Add all words to a deck 
7. Give user deck file


