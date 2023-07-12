from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com/login'

options = webdriver.ChromeOptions()
options.add_argument("--headless")

service = ChromeService(ChromeDriverManager().install())

# Form
with webdriver.Chrome(service=service, options=options) as driver:
    driver.implicitly_wait(10)
    driver.get(url)
    username = driver.find_element(By.ID, "username")
    username.send_keys("foo")
    password = driver.find_element(By.ID, "password")
    password.send_keys("bar")
    submit = driver.find_element(By.CLASS_NAME, 'btn-primary')
    submit.click()
    page_source = driver.page_source

tags = dict()

# Multiple Pages
while True:
    soup = BeautifulSoup(page_source, "html.parser")
    quotes = soup.select(".quote")
    for quote in quotes:
        for tag in quote.select('.tag'):
            if tag.text in tags:
                tags[tag.text] += 1
            else:
                tags[tag.text] = 1
        with open("quotes.txt", "a", encoding="utf-8") as file:
            file.write(quote.select_one('.text').text + '\n')
        file.close()
    if (soup.select_one(".next a") is not None):
        next_page_url = 'https://quotes.toscrape.com/' + soup.select_one(".next a").attrs['href']
        page_source = urlopen(next_page_url)
    else:
        break
 
#Tags
sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)   

#Write the tags to the file
with open("tags.txt", "w") as file:
    file.write('\n'.join('{} {}'.format(x[0], x[1]) for x in sorted_tags))
file.close()

driver.quit()
