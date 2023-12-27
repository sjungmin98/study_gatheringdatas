from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

mongoClient = MongoClient("mongodb://localhost:27017")
database = mongoClient["gatheringdatas"]
collection = database['11st_comments']

webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))

# Navigate to the product page
browser.get("https://www.11st.co.kr/products/pa/4239839553?trTypeCd=Xk&trCtgrNo=70229")

# Scroll to the end of the page to load all comments
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

# Extract comments
comments = browser.find_elements(by=By.CSS_SELECTOR, value="div.c_product_review_cont")

# Iterate through comments and insert into MongoDB
for comment in comments[:10]:
    author = comment.find_element(by=By.CSS_SELECTOR, value="dl.c_product_reviewer > dt.name").text
    option = comment.find_element(by=By.CSS_SELECTOR, value="dl.option_set").text
    rating = comment.find_element(by=By.CSS_SELECTOR, value="div > p.grade").text

    # Check if "더보기" button exists and click it
    show_more_button = comment.find_elements(by=By.CSS_SELECTOR, value="button.c_product_btn.c_product_btn_more6.review-expand-open-text")
    if show_more_button:
        show_more_button[0].click()
        time.sleep(1)  # Add a delay to wait for the content to load

        # Merge content with the additional content
        content = comment.find_element(by=By.CSS_SELECTOR, value="div.cont_text_wrap").text
        additional_content = browser.find_element(by=By.CSS_SELECTOR, value="div.c_product_review_cont div.cont_text_wrap").text
        content += additional_content
    else:
        content = comment.find_element(by=By.CSS_SELECTOR, value="div.cont_text_wrap").text

    # Insert comment into MongoDB
    collection.insert_one({"author": author, "content": content, "rating": rating})

# Close the browser
browser.quit()