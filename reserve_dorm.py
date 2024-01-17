from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from pymongo import MongoClient

# MongoDB 연결 설정
mongoClient = MongoClient("mongodb://192.168.10.240:27017/")
database = mongoClient["AI_LKJ"]
collection = database['reserve_transfer_dorm']

# WebDriver 설정
driver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(driver_manager_directory))
url = "https://www.booking.com/searchresults.ko.html?ss=%EB%B6%80%EC%82%B0&ssne=%EB%B6%80%EC%82%B0&ssne_untouched=%EB%B6%80%EC%82%B0&label=Vit8GNqq0h_49era%7E9RmyvlJBF_JpBNa-QANkJ0NfLVqTd4IsK4wErA%3D%3D&aid=2210273&lang=ko&sb=1&src_elem=sb&src=searchresults&dest_id=-713900&dest_type=city&checkin=2024-01-20&checkout=2024-01-25&group_adults=4&no_rooms=1&group_children=0"
browser.get(url)
time.sleep(10)

# 팝업 닫기
try:
    popup_cancel = browser.find_element(By.CSS_SELECTOR, "#b2searchresultsPage > div.b9720ed41e.cdf0a9297c > div > div > div > div.dd5dccd82f > div.ffd93a9ecb.dc19f70f85.eb67815534 > div > button > span > span > svg > path")
    popup_cancel.click()
except Exception as e:
    print("팝업 닫기 오류:", e)

# 호텔 체크박스 선택
hotel_checkbox = browser.find_element(By.CSS_SELECTOR, "#filter_group_ht_id_\:rs\: > div:nth-child(4) > label > span.ef785aa7f4 > span > svg")
hotel_checkbox.click()
time.sleep(5)

# 페이지 순회 및 데이터 수집
while True:
    elements = browser.find_elements(By.CSS_SELECTOR, 'div.c82435a4b8.a178069f51.a6ae3c2b40.a18aeea94d.d794b7a0f7.f53e278e95.c6710787a4')
    for element in elements:
        print(element.text)
        next_button = browser.find_element(By.CSS_SELECTOR, '#bodyconstraint-inner > div:nth-child(8) > div > div.af5895d4b2 > div.df7e6ba27d > div.bcbf33c5c3 > div.dcf496a7b9.bb2746aad9 > div.d7a0553560 > div.c82435a4b8.a178069f51.a6ae3c2b40.a18aeea94d.d794b7a0f7.f53e278e95.e49b423746 > nav > nav > div > div.b16a89683f.cab1524053 > button')
        next_button.click()
        time.sleep(3)
