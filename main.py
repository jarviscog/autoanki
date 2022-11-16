from AutoAnki import AutoAnki
import os

def main():

    print("Running")
    # sentance = "我的中文名字是朝霖"
    # analyzer = ChineseAnalyzer()
    # result = analyzer.parse('我很高兴认识你')
    # result.tokens()


    db_path = os.path.join('media', 'databases', 'AutoAnki.db')
    # filepath = os.path.join('media', 'chinese')
    filepath1 = os.path.join('media', 'hello.txt')
    filepath2 = os.path.join('media/tt')

    aa = AutoAnki(db_path)

    # aa.add_book(filepath, 'Chinese book😆', notify=False)
    aa.add_book(filepath1, 'Hello.txt😆', notify=False)
    aa.add_book(filepath2, 'This is my first book', notify=False)
    print(aa.book_list)

    aa.update_definitions()

    # # aa.add_book_to_database(os.path.join('media', 'sample_text.txt'), '皮肤颜色。：你好')
    #
    # print("\n")


if __name__ == "__main__":
    main()
