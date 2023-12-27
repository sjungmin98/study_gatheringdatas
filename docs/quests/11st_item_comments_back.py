from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
def dbconnect(collection_name) :
    # MongoDB 클라이언트 설정
    mongoClient = MongoClient("mongodb://localhost:27017")
    database = mongoClient["gatheringdatas"]
    collection = database[collection_name]
    collection.delete_many({})  # 기존 데이터 초기화
    return collection

# 웹 드라이버 설정
webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

# 11번가 상품 페이지로 이동
browser.get("https://www.11st.co.kr/browsing/BestSeller.tmall?method=getBestSellerMain&xfrom=main^gnb#pageNum%%13")

time.sleep(1)  # 페이지가 완전히 로드될 때까지 기다리기
col_11st_items = dbconnect("11st_items")

def collect_and_save_items(browser, collection):
    title = browser.find_element(by=By.CSS_SELECTOR, value="h1.title")
    old_price = browser.find_element(by=By.CSS_SELECTOR, value="dd > del")
    new_price = browser.find_element(by=By.CSS_SELECTOR, value="dd.price > strong > span.value")
    img = 
    details = 
collect_and_save_items(browser, col_11st_items)

def collect_and_save_comments(browser, collection) :
    browser.switch_to.frame("ifrmReview")
    col_11st_items_comments=dbconnect("11st_items_comments")
    comments = browser.find_elements(by=By.CSS_SELECTOR, value=".c_product_review_list > ul > li")
    for comment in comments:
        author = comment.find_element(by=By.CSS_SELECTOR, value="dl > dt.name").text
        rating = comment.find_element(by=By.CSS_SELECTOR, value="div > p.grade").text
        content = comment.find_element(by=By.CSS_SELECTOR, value="div.cont_text_wrap").text
        
        # MongoDB에 댓글 저장
        collection.insert_one({"author": author, "content": content, "rating": rating})

col_11st_items_comments = dbconnect("11st_items_comments")
collect_and_save_comments(browser, col_11st_items_comments)

# 각 상품의 타이틀을 클릭하고, 뒤로 가는 과정을 반복
for i in range(4):
    try:
        element = browser.find_elements(by=By.CSS_SELECTOR, value="div > a > div.pname > p")[i]
        element.click()  # 상품 페이지로 이동
        time.sleep(1)  # 페이지 로딩 대기
        collect_and_save_comments(browser, collection)
        browser.back()  # 이전 페이지 (상품 목록 페이지)로 돌아감
        time.sleep(1)  # 페이지 로딩 대기
    except:
        continue

# 브라우저 종료
browser.quit()
