from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
# options.add_argument('--headless')

#ignores all certificate errors, including self-signed certificate errors in chrome
options.add_argument("--ignore-proxy-certificate-handler")
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

driver.get('https://www.facebook.com/StuyvesantConfessions/')
print("Page loaded")

wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'x1b0d499 x1d69dk1'))) # LOGIN PROMPT CLASS
driver.click(By.CLASS_NAME, 'x1b0d499 x1d69dk1') 
print("Login prompt closed")

wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'xzueoph x1k70j0n'))) # POSTS TAB CLASS
print("Posts loaded")

posts = driver.find_elements(By.CLASS_NAME, 'x78zum5 xdt5ytf xz62fqu x16ldp7u') # POSTS HEADER CLASS
print(f'{len(posts)} post(s) found')

post_data = []

for post in posts:
    name = post.find_element(By.CLASS_NAME, 'profileLink').text
    content = post.find_element(By.CLASS_NAME, 'userContent').text
    post_data.append({'Name': name, 'Content': content})
    print(f'{len(post_data)} post(s) added')

print(post_data)

