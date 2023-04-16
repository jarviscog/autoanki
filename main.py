from AutoAnki import AutoAnki, cli
import os

def main():

    print("Running...")

    db_path = os.path.join('media', 'databases', 'AutoAnki.db')
    aa = AutoAnki(db_path)

    filepath = os.path.join('media', 'hello.txt')
    aa.add_book(filepath, 'My first book😆')

    terminal.terminal_interface("Test")

    print(aa.book_list)

    aa.update_definitions()

    # aa.create_deck()

    # aa.add_book_to_database(os.path.join('media', 'sample_text.txt'), '皮肤颜色。：你好')
    #
    # print("\n")


if __name__ == "__main__":
    main()
