from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
URL = "https://chat.openai.com/"
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--user-data-dir='~/Library/Application Support/Google/Chrome/Profile\ 2'")
chrome_options.add_experimental_option("detach", True)
driver = Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.get(URL)
driver.maximize_window()
new_request_button = driver.find_element(
    By.XPATH,
    "//div[@title='Create New Request']"    
)

time.sleep(200)
new_request_button.click()