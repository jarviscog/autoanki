from AutoAnki import AutoAnki
import os


def main():
    # print("Testing auto-anki")

    db_path = os.path.join('media', 'databases', 'AutoAnki.db')
    filepath = os.path.join('media', 'chinese')


    aa = AutoAnki(db_path)

    aa.add_book(filepath, 'Chinese book😆', notify=False)
    # aa.add_book_to_database(os.path.join('media', 'sample_text.txt'), '皮肤颜色。：你好')


    print("\n")

if __name__ == "__main__":
    main()
