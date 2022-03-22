CREATE TABLE IF NOT EXISTS demo_book_name (
	word_id INTEGER PRIMARY KEY AUTOINCREMENT,
	word VARCHAR(255) NOT NULL UNIQUE,
	number_of_appearances INT,
	CONSTRAINT UQ_word_pinyin UNIQUE(word, pinyin)
)

CREATE TABLE IF NOT EXISTS dictionary(
	word_id INTEGER PRIMARY KEY AUTOINCREMENT,
	word VARCHAR(255) NOT NULL UNIQUE,
	word_traditional VARCHAR(255),
	word_type VARCHAR(255),
	pinyin VARCHAR(255) NOT NULL,
	pinyin_numbers VARCHAR(255),
	number_of_strokes INTEGER,
	sub_components VARCHAR(255),
	frequency FLOAT,
	hsk_level VARCHAR(255),
	top_level VARCHAR(255),
	audio_path VARCHAR(255),
	image_path VARCHAR(255),
	definition VARCHAR(255),
)


ALTER TABLE definitions
ADD CONSTRAINT UQ_word_pinyin UNIQUE(word, pinyin)