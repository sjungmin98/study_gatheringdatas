# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
# ChromeDriver 실행
# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities
# - 주소 https://www.w3schools.com/ 입력
browser.get("https://getbootstrap.com/docs/5.3/examples/checkout/")
# - 가능 여부에 대한 OK 받음
pass
# - html 파일 받음(and 확인)
html = browser.page_source
# - 정보 획득
from selenium.webdriver.common.by import By
# refer official : https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.select.html#module-selenium.webdriver.support.select
from selenium.webdriver.support.ui import Select
# Select(driver.find_element(By.TAG_NAME, "select")).select_by_index(2)

# 국가 selectbox 선택
selector_element = '#country'
element_country = browser.find_element(by=By.CSS_SELECTOR, value=selector_element)
Select(element_country).select_by_index(1)
# 주 selectbox 선택
selector_element = '#state'
element_state = browser.find_element(by=By.CSS_SELECTOR, value=selector_element)
Select(element_state).select_by_index(1)
pass
# browser.save.screenshot("./format.png")
# 브라우저 종료
browser.quit()

# 남의 코드 디버깅시 유의점
# - 환경 겹치지 않게 셋팅(database, version 등)
# - 완전한 업무 파악
# - 명확한 에러 위치 확인(break point 사용)
# # - 미리 현상 실행 (Debug console 사용)