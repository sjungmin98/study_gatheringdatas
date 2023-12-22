from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

# 크롬 드라이버 런타임 경로 지정
driver = webdriver.Chrome()

# WebDriver의 실행이 완료될 떄 까지 최대 5초간 대기
driver.implicitly_wait(5)

# 크롬 브라우저 실행
driver.get("https://www.naver.com")

# Naver 검색 입력창에 입력
driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/div/input").send_keys("Hello Python")

# Naver 검색 버튼 클릭
driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/button").click()

sleep(5)