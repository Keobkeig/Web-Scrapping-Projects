import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service('C:\\Users\\Richie\\Downloads\\chromedriver_win32\\chromedriver.exe') 
options = Options()
options.add_argument('--headless')  
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://scrapingclub.com/exercise/list_infinite_scroll/')
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'col-lg-4.col-md-6.mb-4')))

last_height = driver.execute_script("return document.body.scrollHeight")

#ref: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(20)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
    
products = driver.find_elements(By.CLASS_NAME, 'col-lg-4.col-md-6.mb-4')
clothes_data = []

for product in products:
    name = product.find_element(By.TAG_NAME, 'h4').text
    price = product.find_element(By.TAG_NAME, 'h5').text
    item_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
    image = driver.find_element(By.CLASS_NAME, 'card-img-top').get_attribute('src')
    clothes_data.append({'Product Name': name, 'Product Price': price, 'Product Description': item_link, 'Product Image': image})

for index in range(len(clothes_data)):
    driver.get(clothes_data[index]['Product Description'])
    description = driver.find_element(By.CLASS_NAME, 'card-description').text
    clothes_data[index]['Product Description'] = description

with open('clothes_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['Product Name', 'Product Price', 'Product Description', 'Product Image']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for data in clothes_data:
        writer.writerow(data)
    csvfile.close()

driver.quit()