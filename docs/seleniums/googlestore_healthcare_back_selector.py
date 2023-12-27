# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

webdriver_manager_directory = ChromeDriverManager().install()

# ChromeDriver 실행
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities

# - 주소 https://www.w3schools.com/ 입력
browser.get("https://play.google.com/store/search?q=%ED%97%AC%EC%8A%A4%EC%BC%80%EC%96%B4%EC%95%B1&c=apps&hl=ko-KR&pli=1")

# - 가능 여부에 대한 OK 받음
pass
# - html 파일 받음(and 확인)
html = browser.page_source

# - 정보 획득
from selenium.webdriver.common.by import By
# 앱 제조회사 리스트 : div > a.Si6A0c.Gy4nib
element_companies = browser.find_elements(by=By.CSS_SELECTOR, value="div > a.Si6A0c.Gy4nib")
for company in element_companies:
    company.click()
    time.sleep(1)
    browser.find_element(by=By.CSS_SELECTOR, value="div > h1")       # 화면 완성 term
    browser.back()      # 제품 리스트로 이동
    time.sleep(1)       # 화면 완성 term
    # 앱 상세 제목 : div > h1
    element_title = browser.find_element(by=By.CSS_SELECTOR, value="div > h1")
    print("App company name : {}".format(element_title.text))
    pass
pass

# browser.save.screenshot("./format.png")

# 브라우저 종료
browser.quit()