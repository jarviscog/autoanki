SELECT
chinese_book.book_table_word_id,
dictionary.word,
chinese_book.number_of_appearances
FROM chinese_book
LEFT JOIN dictionary
ON chinese_book.dictionary_word_id = dictionary.word_id