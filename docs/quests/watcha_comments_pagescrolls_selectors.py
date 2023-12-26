# * 웹 크롤링 동작
from pymongo import MongoClient
mongoClient = MongoClient("mongodb://localhost:27017")
database = mongoClient["gatheringdatas"]
collection = database['watcha_comments']
 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
import time

# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities
# - 주소 https://www.w3schools.com/ 입력
browser.get("https://pedia.watcha.com/ko-KR/contents/mV533q5/comments")
# - 가능 여부에 대한 OK 받음
pass
# - html 파일 받음(and 확인)
html = browser.page_source
# - 정보 획득
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
## 한 페이지씩 이동
element_body = browser.find_element(by=By.CSS_SELECTOR, value='body')

previous_scrollHeight = 0
while True :
    element_body.send_keys(Keys.END)

    current_scrollheight = browser.execute_script("return document.body.scrollHeight")
    if previous_scrollHeight >= current_scrollheight:
        break
    else :
        previous_scrollHeight = current_scrollheight
    time.sleep(1)
pass

comments = browser.find_elements(By.CSS_SELECTOR, "ul > div.css-13j4ly.egj9y8a4")

# 컬렉션 데이터 초기화
collection.delete_many({})

for comment in comments[:10]:
    author = comment.find_element(By.CSS_SELECTOR, "div.css-jqudug.egj9y8a3 > div.css-drz8qh.egj9y8a2 > a > div.css-eldyae.e10cf2lr1").text
    content = comment.find_element(By.CSS_SELECTOR, "div.css-2occzs.egj9y8a1 > a > div > span").text
    rating = comment.find_element(By.CSS_SELECTOR, "div.css-jqudug.egj9y8a3 > div.css-31ods0.egj9y8a0 > span").text
    
    collection.insert_one({"author": author, "content": content, "rating": rating})



