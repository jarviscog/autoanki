# from AutoAnki import AutoAnki
# import os
# from chinese import ChineseAnalyzer

from nltk.tokenize.stanford_segmenter import StanfordSegmenter

def main():

    print("Running")
    # sentance = "我的中文名字是朝霖"
    # analyzer = ChineseAnalyzer()
    # result = analyzer.parse('我很高兴认识你')
    # result.tokens()

    segmenter = StanfordSegmenter(path_to_jar="/Users/owner/Documents/PROJECTS/auto-anki/stanford-segmenter-4.2.0.jar",
                                  path_to_model="/Users/owner/Documents/PROJECTS/auto-anki/stanford-segmenter-2020-11-17/dict-chris6.ser.gz")
    segmenter.default_config('zh')
    print(segmenter.segment('哈佛大学的Melissa Dell'))

    # db_path = os.path.join('media', 'databases', 'AutoAnki.db')
    # filepath = os.path.join('media', 'chinese')
    # filepath = os.path.join('media', 'hello.txt')
    # filepath1 = os.path.join('media/tt')
    #
    # aa = AutoAnki(db_path)
    #
    # # aa.add_book(filepath, 'Chinese book😆', notify=True)
    # aa.add_book(filepath1, 'This is my first book', notify=True)
    # print(aa.book_list)
    # # aa.add_book_to_database(os.path.join('media', 'sample_text.txt'), '皮肤颜色。：你好')
    #
    # print("\n")


if __name__ == "__main__":
    main()
