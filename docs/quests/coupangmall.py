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
browser.get('https://www.coupang.com/np/categories/195492?listSize=60&brand=&offerCondition=&filterType=&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=Y&selectedPlpKeepFilter=&sorter=bestAsc&filter=&component=195392&rating=0')
# - 가능 여부에 대한 OK 받음
pass
# - 정보 획득
from selenium.webdriver.common.by import By
# selector_value = "#ty_thmb_view > ul > li:nth-child(1) > div > a > div.mnemitem_tit > span.mnemitem_goods_tit"
##여러개 elements 정보 가져오기
selector_value = "div.name" 
elements_path = browser.find_elements(by=By.CSS_SELECTOR, value=selector_value)
type(elements_path)
pass
for webelement in elements_path:
    title = webelement.text
    print(title)
pass
browser.quit()