from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

webdriver_manager_directory = ChromeDriverManager().install()

chrome_options = Options()

# User-Agent 설정
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory), options=chrome_options)

# 1~10 페이지까지 순회
for i in range(1, 11):
    url = "https://www.coupang.com/np/campaigns/348?page={}".format(i)
    browser.get(url)
    time.sleep(2)  # 페이지 로딩 대기

browser.quit()