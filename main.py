from AutoAnki import AutoAnki
import os


def main():
    # print("Testing auto-anki")

    db_path = os.path.join('media', 'databases', 'AutoAnki.db')
    filepath = os.path.join('media', 'chinese')
    filepath = os.path.join('media', 'hello.txt')
    filepath1 = os.path.join('media/tt')

    aa = AutoAnki(db_path)

    # aa.add_book(filepath, 'Chinese book😆', notify=True)
    aa.add_book(filepath1, 'This is my first book', notify=True)
    print(aa.book_list)
    # aa.add_book_to_database(os.path.join('media', 'sample_text.txt'), '皮肤颜色。：你好')

    print("\n")
    aa.update_definitions()


if __name__ == "__main__":
    main()
