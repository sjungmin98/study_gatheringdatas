from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# MongoDB 클라이언트 설정
mongoClient = MongoClient("mongodb://localhost:27017")
database = mongoClient["gatheringdatas"]
collection = database['11st_comments']
collection.delete_many({})  # 기존 데이터 초기화

# 웹 드라이버 설정
webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

# 11번가 상품 페이지로 이동
browser.get("https://www.11st.co.kr/products/pa/4239839553?trTypeCd=Xk&trCtgrNo=70229")

# 리뷰 iframe으로 전환
browser.switch_to.frame("ifrmReview")

# 페이지 끝까지 스크롤
def scroll_to_end(browser):
    element_body = browser.find_element(by=By.CSS_SELECTOR, value='body')
    previous_scrollheight = 0
    while True:
        element_body.send_keys(Keys.END)
        time.sleep(2)  # 스크롤 후 페이지 로딩을 위해 대기
        current_scroll_height = browser.execute_script("return document.body.scrollHeight")
        if previous_scrollheight == current_scroll_height:
            break
        previous_scrollheight = current_scroll_height

scroll_to_end(browser)

# 댓글 수집 및 저장
def collect_and_save_comments(browser, collection):
    comments = browser.find_elements(by=By.CSS_SELECTOR, value=".c_product_review_list > ul > li")[:10]
    for comment in comments:  # 여기에서 index를 제거했습니다
        author = comment.find_element(by=By.CSS_SELECTOR, value="dl > dt.name").text
        rating = comment.find_element(by=By.CSS_SELECTOR, value="div > p.grade").text
        content = comment.find_element(by=By.CSS_SELECTOR, value="div.cont_text_wrap").text
        
        # '더보기' 버튼 클릭 시도
        try:
            show_more_button = comment.find_elements(by=By.CSS_SELECTOR, value="button.c_product_btn.c_product_btn_more6.review-expand-open-text")
            if show_more_button:
                show_more_button[0].click()
                time.sleep(1)  # 클릭 후 동적 로드 대기
                additional_content = comment.find_element(by=By.CSS_SELECTOR, value="div.cont_text_wrap").text
                content += " " + additional_content
        except:
            pass 
        
        # MongoDB에 댓글 저장
        collection.insert_one({"author": author, "content": content, "rating": rating})

collect_and_save_comments(browser, collection)

# 브라우저 종료
browser.quit()