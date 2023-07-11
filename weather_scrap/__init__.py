from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

url = "http://www.nysmesonet.org/weather/today_stats"

options = webdriver.ChromeOptions()
options.add_argument("--headless")

service = ChromeService(ChromeDriverManager().install())

with webdriver.Chrome(service=service, options=options) as driver:
    driver.get(url)
    time.sleep(5) 
    page_source = driver.page_source

soup = BeautifulSoup(page_source, "html.parser")

tables = soup.find_all("table", {"class": "table table-sm table-hover data-table w-100"})

warmest_high = tables[0]
coldest_low = tables[3]

weather_dict = {}
# Extract warmest high data
for row in warmest_high.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) >= 3:
        station = cells[1].get_text(strip=True)
        value = cells[2].get_text(strip=True)
        weather_dict[station] = {"Warmest High": value}

for row in coldest_low.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) >= 3:
        station = cells[1].get_text(strip=True)
        value = cells[2].get_text(strip=True)
        if station in weather_dict:
            weather_dict[station]["Coldest Low"] = value
        else:
            weather_dict[station] = {"Warmest High": "NaN", "Coldest Low": value}

# Write the dictionary to a CSV file
output_file = "weather.csv"
with open(output_file, "w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["Area", "Warmest High", "Coldest Low"])
    for area, data in weather_dict.items():
        writer.writerow([area, data.get("Warmest High", "NaN"), data.get("Coldest Low", "NaN")])

driver.quit()


