CREATE TABLE IF NOT EXISTS BOOK_NAME (
    book_table_word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dictionary_word_id INTEGER NOT NULL UNIQUE REFERENCES dictionary(word_id),
    number_of_appearances INT
)
