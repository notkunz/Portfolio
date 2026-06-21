from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
import time

URL = "https://noungeeks.com/download-noun-e-courseware-course-materials-for-all-department/"

download_folder = "NOUN_Materials"
os.makedirs(download_folder, exist_ok=True)

driver = webdriver.Chrome()
driver.get(URL)

time.sleep(5)

downloaded = set()

while True:
    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    for row in rows:
        try:
            cols = row.find_elements(By.TAG_NAME, "td")

            course_code = cols[0].text.strip()

            link = cols[1].find_element(By.TAG_NAME, "a")
            href = link.get_attribute("href")

            if href not in downloaded:
                print(f"Downloading {course_code}")

                r = requests.get(href)

                with open(f"{download_folder}/{course_code}.pdf", "wb") as f:
                    f.write(r.content)

                downloaded.add(href)

        except Exception as e:
            print(e)

    # next page
    try:
        next_btn = driver.find_element(By.ID, "tablepress-1_next")
        if "disabled" in next_btn.get_attribute("class"):
            break

        next_btn.click()
        time.sleep(3)

    except:
        break

driver.quit()

print("Done")