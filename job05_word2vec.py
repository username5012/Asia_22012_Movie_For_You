import pandas as pd
from gensim.models import Word2Vec

review_word = pd.read_csv('./crawling_data/one_sentences.csv')
review_word.info()

one_sentence_reviews = list(review_word['reviews'])
cleaned_tokens = []
for sentence in one_sentence_reviews:
    token = sentence.split()
    cleaned_tokens.append(token)


embedding_model = Word2Vec(cleaned_tokens, vector_size = 100,
                           window=4, min_count = 20,
                           workers = 4, epochs = 100, sg=1)
# Word2Vec : 단어를 차원화함
# vector는 방향과 크기가 있음. | 계산법 : (x^2+y^2....)^0.5
# min_count : 학습할 단어의 최소 빈도수
# window는 Conv1D의 Kernel_size와 비슷한 맥락
# workers = 처리시에 사용할 CPU/GPU 스레드 갯수
# sg (= skip-gram) : 중심 단어로 주변 단어 의미 추측  | CBOW : 주변 단어로 중심 단어 의미 추측    / sg = 1 == sg = True

embedding_model.save('./models/word2vec_movie_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))


