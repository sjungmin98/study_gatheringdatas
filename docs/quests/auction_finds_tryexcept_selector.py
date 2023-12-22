from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(driver_manager_directory))
auction_url = "https://corners.auction.co.kr/corner/categorybest.aspx"
browser.get(auction_url)

from selenium.webdriver.common.by import By
product_info_selector = "div.info"
product_elements = browser.find_elements(by=By.CSS_SELECTOR, value=product_info_selector)



for product_element in product_elements: 
    title_selector = "em"
    title_element = product_element.find_element(by=By.CSS_SELECTOR, value=title_selector)
    product_title = title_element.text

   
    try:
        old_price_selector = "span.cost"
        old_price_element = product_element.find_element(by=By.CSS_SELECTOR, value=old_price_selector)
        original_price = old_price_element.text
    except:
        original_price = ""

   
    try:
        new_price_selector = "span.sale"
        new_price_element = product_element.find_element(by=By.CSS_SELECTOR, value=new_price_selector)
        discounted_price = new_price_element.text
    except:
        discounted_price = ""

    
    try:
        delivery_method_selector = "div.item_icons"
        delivery_method_element = product_element.find_element(by=By.CSS_SELECTOR, value=delivery_method_selector)
        delivery_method = delivery_method_element.text.split()
        pass
    except:
        delivery_method = ""

    print("title : {}, old price : {}, new price : {}, delivery : {}".format(product_title, original_price, discounted_price, delivery_method)) 

browser.quit()