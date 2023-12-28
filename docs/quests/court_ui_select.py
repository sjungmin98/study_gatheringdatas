from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pymongo import MongoClient
import time

def gather_court_data():
    # 웹드라이버 매니저로부터 크롬드라이버의 설치 경로를 가져옵니다.
    webdriver_manager_directory = ChromeDriverManager().install()

    # 크롬드라이버를 실행합니다.
    browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

    # 법원 경매 사이트에 접속합니다.
    browser.get("https://www.courtauction.go.kr/")

    # 메인 프레임으로 전환합니다.
    browser.switch_to.frame('indexFrame')

    # '법원별 기일표' 메뉴를 클릭합니다.
    browser.find_element(by=By.CSS_SELECTOR, value="#menu > h1:nth-child(5) > a > img").click()

    # 법원/소재지 리스트를 가져옵니다.
    element_courts = browser.find_elements(by=By.CSS_SELECTOR, value="#idJiwonNm > option")

    # MongoDB 클라이언트 설정
    mongoClient = MongoClient("mongodb://localhost:27017")
    database = mongoClient["gatheringdatas"]
    collection = database['court_ui_select']
    collection.delete_many({})  # 기존 데이터 초기화

    # 법원 리스트 중 상위 3개만 처리합니다.
    for index in range(3):
        # 법원을 선택합니다.
        select_court = Select(browser.find_element(by=By.CSS_SELECTOR, value="#idJiwonNm")) 
        select_court.select_by_index(index)
        
        # '검색' 버튼을 클릭합니다.
        url = "#contents > form > div.tbl_btn > a:nth-child(1) > img"
        browser.find_element(by=By.CSS_SELECTOR, value=url).click()
        time.sleep(0.5)

        # 법원소재지, 사건번호, 소재지 및 내역을 추출합니다.
        court_location = browser.find_element(by=By.CSS_SELECTOR, value='#search_title > ul > li:nth-child(2)').text
        case_numbers = browser.find_elements(by=By.CSS_SELECTOR, value='#contents > div.table_contents > form:nth-child(1) > table > tbody > tr > td:nth-child(2)')
        locations_and_details = browser.find_elements(by=By.CSS_SELECTOR, value='#contents > div.table_contents > form:nth-child(1) > table > tbody > tr > td:nth-child(4)')
        
        # 추출한 데이터를 MongoDB에 저장합니다.
        for i in range(len(case_numbers)):
            data = {
                '법원소재지': court_location,
                '사건번호': case_numbers[i].text,
                '소재지 및 내역': locations_and_details[i].text
            }
            collection.insert_one(data)

        # 이전 화면으로 돌아갑니다.
        url = "#contents > div.table_contents > form:nth-child(1) > div > div > a:nth-child(5) > img"
        browser.find_element(by=By.CSS_SELECTOR, value=url).click()
        time.sleep(3)

    # 웹 브라우저를 종료합니다.
    browser.quit()
    
    # Collection을 반환합니다.
    return collection

# 함수를 실행합니다.
gather_court_data()
