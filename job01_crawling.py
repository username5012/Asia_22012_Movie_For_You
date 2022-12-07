from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)

# years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022']
url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page=1'



