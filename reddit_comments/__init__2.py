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

service = Service('C:\\Users\\Richie\\Downloads\\chromedriver_win32\\chromedriver.exe') 
options = Options() 
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")

driver = webdriver.Chrome(service=service, options=options)

df = pd.read_csv('interesting.txt', header=None)
df.columns = ['url']

for url in df['url']:
    driver.get(url)
    page_source = driver.page_source
    print(df[df['url'] == url].index[0]) #progess bar
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='entry unvoted']")))
    soup = BeautifulSoup(driver.page_source, "html.parser")

    title = soup.find("title").text
    description = soup.find("meta", attrs={"name": "description"})['content']
    df.loc[df['url'] == url, 'title'] = title
    df.loc[df['url'] == url, 'description'] = description

driver.quit()

df.to_csv('task2.csv', index=False)
    