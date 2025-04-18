from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import re
import csv
from typing import List

class Configs:
    class EASY:
        URL = 'https://www3.nhk.or.jp/news/easy'
        XPATH_ARTICLES = '//*[@class="news-list__item"]//h2'
        XPATH_PARAGRAPH = "//div[@class='article-body']/p"
        DELIMITER = ''
        MIN_CHAR_COUNT = 5
        MAX_CHAR_COUNT = 60

    class HARD:
        URL = 'https://www3.nhk.or.jp/news/cat06.html'
        XPATH_ARTICLES = "//*[@class='module--content']//em[@class='title']"
        XPATH_PARAGRAPH = '//*[@class="content--detail-body"]'
        DELIMITER = '。'
        MIN_CHAR_COUNT = 5
        MAX_CHAR_COUNT = 50
class CACHE:
    headline_set = None
class CONSTANTS:
    INNER_HTML = "innerHTML"
    ARTICLE_COUNT_LIMIT = 3

CURR_CONFIG = Configs.EASY

def totalLength(str_list:List[str]):
    return sum(map(lambda x: len(x), str_list))

def maybeSplit(sentence:str):
    if(sentence <= CURR_CONFIG.MAX_CHAR_COUNT): return [sentence]
    phrases = sentence.split('、')
    ptr_start = 0
    ptr_end = len(phrases - 1)
    curr_ptr = ptr_start
    part1 = []
    part2 = []
    curr_part = part1
    while(len(part1) + len(part2) < len(phrases)):
        curr_part.append(phrases[curr_ptr])
        if(totalLength(part1) < totalLength(part2)):
            curr_part = part1
            curr_ptr = ptr_start + 1
        else:
            curr_part = part2
            curr_ptr = ptr_end - 1

def split_more(sentence_list):
    ret = []
    for sentence in sentence_list:
        for phrase in maybeSplit(sentence):
            ret.append(phrase)
    return ret

def get_2d_sentence_list(articles):
    sentence_list_2d = []
    for article in articles:
        sentence_list = re.split('。|\s+', article)
        sentence_list = map(
            lambda x: x.strip(),
            sentence_list
        )
        sentence_list = filter(
            lambda x: type(x) == str and len(x) > 5,
            sentence_list
        )
        sentence_list = list(sentence_list)
        # sentence_list = split_more(sentence_list)
        sentence_list_2d.append(sentence_list)
    return sentence_list_2d

def get_yesterday_string():
    from datetime import datetime, timedelta
    yesterday = datetime.now() - timedelta(4)
    return yesterday.strftime('%Y-%m-%d')

def clean(inner_html):
    text = re.sub(r"<rt>.*?</rt>", '', inner_html)
    # replace tags with delimiter
    return re.sub(r"<.*?>", CURR_CONFIG.DELIMITER, text)

def loadFinishedHeadlines():
    CACHE.headline_set = set()
    with open('./input/finishedHeadlines2.tsv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for idx, row in enumerate(list(reader)):
            CACHE.headline_set.add(row[0].strip())

def shouldSkip(headlineTxt):
    if(not CACHE.headline_set):
        print('loading')
        loadFinishedHeadlines()
    print(headlineTxt)
    return headlineTxt in CACHE.headline_set

def saveHeadlines(headlineList):
    with open('./input/currentHeadlines.tsv', 'w') as f:
        f.write('\n'.join(headlineList))

def get_articles(start_index = 0):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    try:
        articles = []
        time.sleep(3)

        driver.get(CURR_CONFIG.URL)
        
        driver.maximize_window()
        time.sleep(3)
        articleElements = driver.find_elements(
            By.XPATH, 
            CURR_CONFIG.XPATH_ARTICLES
        )

        headlineList = []
        for index, element in enumerate(articleElements):
            if(len(headlineList) >= CONSTANTS.ARTICLE_COUNT_LIMIT):
                break
            if(index < start_index): continue
            sentence_list = []
            headlineTxt = element.get_attribute('innerHTML')
            headlineTxt = f'{clean(headlineTxt).strip()}'
            
            if(shouldSkip(headlineTxt)):
                continue
            headlineList.append(headlineTxt)
            print(headlineTxt)
            sentence_list.append(f'{headlineTxt}。')

            element.click()
            time.sleep(6)

            p_elements = driver.find_elements(
                By.XPATH,
                CURR_CONFIG.XPATH_PARAGRAPH
            )

            for p_element in p_elements:
                paragraph_html = p_element.get_attribute('innerHTML')
                sentence_list.append(clean(paragraph_html).strip())

            articles.append("".join(sentence_list))
            driver.back()
            time.sleep(3)
        articles = get_2d_sentence_list(articles)
        print(articles)
        saveHeadlines(headlineList)
        driver.quit()
        return articles
    except Exception as e:
        print(e)
        driver.quit()

# get_articles()