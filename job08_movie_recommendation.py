import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)  # simScore를 유사도 높은 순으로 sort.
    simScore = simScore[:11]                 # 자기 자신을 포함하기 때문에 출력하고 싶은 영화 갯수 + 1을 줘야함 ([:11] -> [0]~[10] 11개 추출)
    movie_idx = [i[0] for i in simScore]     # [0] = 영화의 Index가 들어있음. |  [1] = 영화 유사도
    recMovieList = df_reviews.iloc[movie_idx, 0]  # df_reviews의 컬럼_0 = 영화 제목
    return recMovieList

df_reviews = pd.read_csv('./crawling_data/one_sentences.csv')
tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    tfidf = pickle.load(f)

# < 영화 제목 이용 >
movie_idx = df_reviews[df_reviews['titles']=='겨울왕국 2 (Frozen 2)'].index[0]  # 제목이 ''인 영화의 Index 번호 (ex. 코코 -> 2944, 모아나 -> 476)
cosin_sim = linear_kernel(tfidf_matrix[movie_idx], tfidf_matrix)    # cosin_sim : 코사인 유사도  | # linear_kernel : 코사인값 계산
print(cosin_sim)
recommendation = getRecommendation(cosin_sim)
print(recommendation[1:11])


# sin : 높이 / 빗변
# cos : 밑변 / 빗변  |   cos값은 0도 : 1, 90도 : 0,   180도 : -1
# 코사인 유사도 : 두 점 간의 cos 값을 통해 연관성을 파악할 수 있다. | 1에 가까울 수록 동일한 의미. -1에 가까울 수록 상반된 의미. 0은 연관성 X
# tan : 높이 / 밑변



# < Keyword 이용 >
# embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
# key_word = '송강호'
# sim_word = embedding_model.wv.most_similar(key_word, topn=10)
# words = [key_word]
# for word, _ in sim_word:
#     words.append(word)
# print(words)
# sentence = []
# count = 11
# for word in words:
#     sentence = sentence + [word] * count
#     count -= 1
# sentence = ' '.join(sentence)
# sentence_vec = tfidf.transform([sentence])
# cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation)
#
#
# < 문장 이용 => 전처리 작업 필요>
# sentence = '화려한 액션과 소름 돋는 반전이 있는 영화'
# review = re.sub('[^가-힣 ]', ' ', sentence)
# okt = Okt()
# token = okt.pos(review, stem=True)
# df_token = pd.DataFrame(token, columns=['word', 'class'])
# df_token = df_token[(df_token['class']=='Noun') |
#                     (df_token['class']=='Verb') |
#                     (df_token['class']=='Adjective')]
# words = []
# for word in df_token.word:
#     if 1 < len(word):
#         words.append(word)
# cleaned_sentence = ' '.join(words)
# print(cleaned_sentence)
# sentence_vec = tfidf.transform([cleaned_sentence])
# cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation)

