from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time

# MongoDB 클라이언트 설정
mongoClient = MongoClient("mongodb://192.168.10.240:27017/")
# database 연결
database = mongoClient["AI_LKJ"]
# collection 작업
collection = database['reserve_dorm']
collection.delete_many({})

# 웹드라이버 세팅
driver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(driver_manager_directory))
url = "https://www.agoda.com/ko-kr/search?guid=903f75e4-12e7-486b-a8a8-4eafa96d42b9&asq=h83K5OpxMgwyDRBM%2B68DD5ufa9Vwpz6XltTHq4n%2B9gMIhr%2FHdI3Zp6E1hg81WRuFJtXlxDYuVQBv7pSWXIJjpqjBuHI3PJN3QnlJvOTuCIv9KtNCnQMUNDlNUEPib3uQr6QDs48C6hOjLzuYUvlEgOm%2B3QacrQMDUE7JkJAfzu2gtrYMgXaJ%2F3RhDDtVGUZGXrPk1JS%2BVyCMDKsWGu5iag%3D%3D&city=17172&tick=638409987630&locale=ko-kr&ckuid=918d2837-99d3-4469-94f9-b7089ef00e1d&prid=0&currency=KRW&correlationId=bf32119c-6047-4b1f-bf5d-7cc840c6f227&analyticsSessionId=7405222636290426852&pageTypeId=1&realLanguageId=9&languageId=9&origin=KR&cid=1908612&userId=918d2837-99d3-4469-94f9-b7089ef00e1d&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=26&currencyCode=KRW&htmlLanguage=ko-kr&cultureInfoName=ko-kr&machineName=hk-pc-2f-acm-web-user-b6b5986bf-wbs6s&trafficGroupId=4&sessionId=mktgv1kzvzcw1fclmcsrmvhx&trafficSubGroupId=849&aid=296180&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&browserFamily=Chrome&cdnDomain=agoda.net&checkIn=2024-01-20&checkOut=2024-01-25&rooms=1&adults=4&children=0&priceCur=KRW&los=5&textToSearch=%EB%B6%80%EC%82%B0&travellerType=3&familyMode=off&ds=PcYZuuOnxggxbWZI&productType=-1"
browser.get(url)

# 특정 요소가 로드될 때까지 대기
WebDriverWait(browser, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#searchPageReactRoot"))
)

# 호텔 체크박스 클릭
try:
    # 첫 번째 선택자로 체크박스 클릭 시도
    checkbox = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#SideBarLocationFilters > div:nth-child(3) > div.filter-items > ul > li:nth-child(3) > span > span:nth-child(1) > span")))
    checkbox.click()
except NoSuchElementException:
    # 첫 번째 선택자로 체크박스를 찾지 못할 경우, 두 번째 선택자로 체크박스 클릭 시도
    try:
        checkbox = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#SideBarLocationFilters > div:nth-child(2) > div.filter-items > ul > li:nth-child(3) > span > span:nth-child(1) > span")))
        checkbox.click()
    except NoSuchElementException:
        # 두 번째 선택자로도 체크박스를 찾지 못할 경우, 세 번째 선택자로 체크박스 클릭 시도
        try:
            checkbox = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#SideBarLocationFilters > div:nth-child(1) > div.filter-items > ul > li:nth-child(1) > span > span:nth-child(1) > span")))
            checkbox.click()
        except NoSuchElementException:
            print("체크박스를 찾을 수 없습니다.")

browser.quit()