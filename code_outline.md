##Database structure:

dictionary:
- word_id
- word
- traditional
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
------
book_name
 - id
 - word
 - number_of_appearances


##PageScraper: Scrape library websites for segments of book
    Current usable websites:
        www.99csw.com
        m.xyyuedu.com
    Read book index page for page links (usually book chapters)
    Store pages as files in './pages/website_name/book_name'

##Database builder: Get json files and store words in database, get assets for dictionary table
    Add segments together until 300kb limit is hit
    Send to pinyin converter and download the converted file
    add words from file into the database table for that book
    take words from book table and store them in definitions table

##Deck Maker: Take database entries to make a deck
    Take book name(s) as input
    Read the table for the book in the database.
    For each word, read from the definitions table to get all other information
    Create notes for every word
    Add all words to a deck
    Give user deck file


