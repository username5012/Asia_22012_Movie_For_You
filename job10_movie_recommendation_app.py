import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from PyQt5.QtCore import QStringListModel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import linear_kernel


form_window = uic.loadUiType('./movie_recommendation_app.ui')[0]

class Exam(QWidget, form_window):  # class ~ def 라인만 의미를 가지고 있는 문장.
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 모델 로딩
        self.tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()
        with open ('./models/tfidf.pickle', 'rb') as f:
            self.tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')

        # ComboBox에 타이틀 설정
        self.df_reviews = pd.read_csv('./crawling_data/one_sentences.csv')
        self.titles = self.df_reviews['titles']
        self.titles = sorted(self.titles)
        for title in self.titles:
            self.combo_box.addItem(title)

        # 타이틀 자동 완성
        model = QStringListModel()
        model.setStringList(self.titles)               # ()안에는 필요한 대상 | () 안에는 list or series 형태
        completer = QCompleter()
        completer.setModel(model)
        self.line_edit.setCompleter(completer)

        # Slot 연결
        self.combo_box.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommend.clicked.connect(self.btn_slot)


    def recommendation_by_movie_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        cosin_sim = linear_kernel(self.tfidf_matrix[movie_idx], self.tfidf_matrix)
        recommendation = self.getRecommendation(cosin_sim)
        recommendation = '\n'.join(list(recommendation[1:]))
        self.lbl_recommend.setText(recommendation)


    def combobox_slot(self):
        title = self.combo_box.currentText()
        self.recommendation_by_movie_title(title)

    def btn_slot(self):
        key_word = self.line_edit.text()

        # title로 검색할 때,
        if key_word in self.titles:
            self.recommendation_by_movie_title(key_word)

        # 리뷰 키워드로 검색할 때,
        elif key_word in list(self.embedding_model.wv.index_to_key):
            sim_word = self.embedding_model.wv.most_similar(key_word, topn=10)
            words = [key_word]
            for word, _ in sim_word:
                words.append(word)
            sentence = []
            count = 11
            for word in words:
                sentence = sentence + [word] * count
                count -= 1
            sentence = ' '.join(sentence)
            sentence_vec = self.tfidf.transform([sentence])
            cosin_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
            recommendation = self.getRecommendation(cosin_sim)
            recommendation = '\n'.join(list(recommendation[:10]))
            self.lbl_recommend.setText(recommendation)







    # 추천 함수
    def getRecommendation(self, cosin_sim):

        simScore = list(enumerate(cosin_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # simScore를 유사도 높은 순으로 sort.
        simScore = simScore[:11]  # 자기 자신을 포함하기 때문에 출력하고 싶은 영화 갯수 + 1을 줘야함 ([:11] -> [0]~[10] 11개 추출)
        movie_idx = [i[0] for i in simScore]  # [0] = 영화의 Index가 들어있음. |  [1] = 영화 유사도
        recMovieList = self.df_reviews.iloc[movie_idx, 0]  # df_reviews의 컬럼_0 = 영화 제목
        return recMovieList







if __name__ == "__main__":

    app = QApplication(sys.argv)   #Qapplication : PyQt5 내부 어플리케이션
    mainWindow = Exam()            # 해당 라인에서 객체가 생성됨
    mainWindow.show()              # .show : 화면에 출력하도록 하는 명령
    sys.exit(app.exec_())          # (app.exec_()) : 해당 프로그램 종료.
                                   # app ~ exec_()) 까지가 위젯에 쓰이는 모듈.