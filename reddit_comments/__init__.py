import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = "https://old.reddit.com/r/InternetIsBeautiful/comments/"

service = Service('C:\\Users\\Richie\\Downloads\\chromedriver_win32\\chromedriver.exe') 
options = Options() 
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=service, options=options)

urls = []

def get_links(url):
    driver.get(url)
    page_source = driver.page_source

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='entry unvoted']")))
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = driver.find_elements(By.XPATH, '//*[@data-type="comment"]/p/a[2]')
    
    comments = soup.find_all("div", class_="entry unvoted")
 
    for comment in comments:
        body = comment.find("div", class_="md").text
        if (re.search(r'\b(?:awesome|fun|wow|amazing|love)\b', body)):
            link = links[comments.index(comment)].get_attribute('href')
            urls.append(link)
    
    next_page = soup.find("span", class_="next-button")
    print(next_page)
    if next_page:
        next_page_link = next_page.find("a").attrs['href']
        get_links(next_page_link)
    
get_links(url)
driver.quit()

df = pd.DataFrame(urls)
df.to_csv('interesting.txt', index=False, header=False)

