from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import re
import csv

NHK_NEWS_EASY_URL = 'https://www3.nhk.or.jp/news/easy'

class Configs:
    class EASY:
        URL = 'https://www3.nhk.or.jp/news/easy'
        XPATH_ARTICLES = '//*[@class="news-list__item"]//h2'
        XPATH_PARAGRAPH = "//div[@class='article-body']/p"

    class HARD:
        URL = 'https://www3.nhk.or.jp/news/cat06.html'
        XPATH_ARTICLES = "//*[@class='module--content']//em[@class='title']"
        XPATH_PARAGRAPH = '//*[@class="content--detail-body"]'

CURR_CONFIG = Configs.EASY

def get_yesterday_string():
    from datetime import datetime, timedelta
    yesterday = datetime.now() - timedelta(4)
    return yesterday.strftime('%Y-%m-%d')

class CACHE:
    headline_set = None
class CONSTANTS:
    INNER_HTML = "innerHTML"
    ARTICLE_COUNT_LIMIT = 3

def clean(inner_html):
    text = re.sub(r"<rt>.*?</rt>", '', inner_html)
    return re.sub(r"<.*?>", "", text)

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
        
        saveHeadlines(headlineList)
        driver.quit()
        return articles
    except Exception as e:
        print(e)
        driver.quit()

# get_articles()