import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc
from PIL import Image
import matplotlib as mpl

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus'] = False
rc('font', family=font_name)

df = pd.read_csv('./crawling_data/one_sentences.csv')
words = df[df['titles']=='라이크 크레이지 (Like Crazy)']['reviews']
print(words.iloc[0])
words = words.iloc[0].split()
print()

worddict = collections.Counter(words)   # 출연 빈도   | .unique와 비슷함.
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(background_color='white', max_words=2000,
                          font_path=font_path).generate_from_frequencies(worddict)
plt.figure(figsize=(12,12))
plt.imshow(wordcloud_img, interpolation='bilinear')  # interpolation : 이미지 처리 방식 | interpolation = 'bilinear' : 부드럽게
plt.axis('off')
plt.show()


