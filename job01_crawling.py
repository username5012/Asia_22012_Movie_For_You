from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

# years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
your_year = 2022

review_num_path = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
review_button_xpath = '//*[@id = "movieEndTabMenu"]/li[6]/a'
review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'


for page in range(1,32):
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year, page)
    titles = []
    reviews = []
    try:
        for title_num in range(1 ,21):
            driver.get(url)
            time.sleep(0.5)
            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(title_num)
            title = driver.find_element('xpath', movie_title_xpath).text
            driver.find_element('xpath', movie_title_xpath).click()
            time.sleep(0.1)
            try:
                driver.find_element('xpath', review_button_xpath).click()
                time.sleep(0.1)
                review_num = driver.find_element('xpath', review_num_path).text
                review_num = review_num.replace(',', '')
                review_range = (int(review_num) - 1)// 10 + 1
                if review_range > 3:
                    review_range = 3

                for review_page_num in range (1, review_range + 1):
                    review_page_button_xpath = '// *[ @ id = "pagerTagAnchor{}"]'.format(review_page_num)
                    driver.find_element('xpath', review_page_button_xpath).click()
                    time.sleep(0.1)

                    for review_title_num in range(1,11):
                            review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(review_title_num)
                            driver.find_element('xpath', review_title_xpath).click()
                            time.sleep(0.1)
                            try:
                                review = driver.find_element('xpath', review_xpath).text
                                titles.append(title)
                                reviews.append(review)
                                print(title)
                                print(review)
                                driver.back()
                            except:
                                print('review',page, title_num, review_title_num)
                                driver.back()
            except:
                print('review button', page, title_num)


        df = pd.DataFrame({'titles':titles, 'reviews':reviews})
        df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, page), index=False)

    except:
        print('error', page, title_num)

