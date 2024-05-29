-- Here is all of the fields that a card could have:
-- word
-- word traditional 
-- pinyin
-- pinyin numbers
-- zhuyin
-- jyutping 
-- part of speech
-- number of strokes
-- sub components
-- definition
-- frequency
-- HSK level
-- tocfl level
-- audio path
-- image path
-- character graphic
-- examples

CREATE TABLE IF NOT EXISTS dictionary(
	word_id INTEGER PRIMARY KEY AUTOINCREMENT,
	word VARCHAR(255) NOT NULL UNIQUE,
	word_traditional VARCHAR(255),
	pinyin VARCHAR(255),
	pinyin_numbers VARCHAR(255),
	zhuyin VARCHAR(255),
	jyutping VARCHAR(255),
	part_of_speech VARCHAR(255),
	number_of_strokes INTEGER,
	sub_components VARCHAR(255),
	definition VARCHAR(255),
	frequency FLOAT,
	hsk_level VARCHAR(255),
	tocfl_level VARCHAR(255),
	audio_path VARCHAR(255),
	image_path VARCHAR(255),
	character_graphic VARCHAR(255),
	examples VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS book_list(
    book_name VARCHAR(255),
    table_name VARCHAR(255),
    language VARCHAR(100)
);


--In the future make is so that BOTH have to be unique
--ALTER TABLE definitions
--ADD CONSTRAINT UQ_word_pinyin UNIQUE(word, pinyin)


--Select b.dictionary_word_id, d.word, d.word_traditional, d.word_type, d.pinyin, d.pinyin_numbers, d.hsk_level, d.definition
--FROM book_table b
--INNER JOIN dictionary d ON b.dictionary_word_id = d.word_id
