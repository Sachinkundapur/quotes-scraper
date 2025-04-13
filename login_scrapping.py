import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("LOGIN_USERNAME")
PASSWORD = os.getenv("LOGIN_PASSWORD")

# Setup
driver = webdriver.Chrome()

url = "https://quotes.toscrape.com/login"
driver.get(url)
time.sleep(1)

# Login
driver.find_element(By.ID, "username").send_keys("Sachin")
driver.find_element(By.ID, "password").send_keys("Imsachin@271527")
driver.find_element(By.CLASS_NAME, "btn-primary").click()
time.sleep(1)

# Collect tag URLs
tag_links = driver.find_elements(By.CSS_SELECTOR, ".tag-item a")
tag_urls = [tag.get_attribute("href") for tag in tag_links]

# Prepare CSV file
with open("quotes_scraped.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["Tag", "Text", "Author", "About_link", "Goodreads Page Link", "Inside Quote Tags"])
    writer.writeheader()

    # Loop through each tag page
    for link in tag_urls:
        driver.get(link)
        tag_name = link.split("/")[-2].strip()
        print("🔖 Tag:", tag_name)

        while True:
            time.sleep(1)
            quotes = driver.find_elements(By.CLASS_NAME, "quote")

            for quote in quotes:
                try:
                    text = quote.find_element(By.CLASS_NAME, "text").text
                except:
                    text = ""

                try:
                    author = quote.find_element(By.CLASS_NAME, "author").text
                except:
                    author = ""

                try:
                    about_link = quote.find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
                except:
                    about_link = ""

                try:
                    goodreads_page_link = quote.find_elements(By.TAG_NAME, "a")[1].get_attribute("href")
                except:
                    goodreads_page_link = ""

                try:
                    inside_tag = quote.find_element(By.CLASS_NAME, "tags").text.split()[1:]
                except:
                    inside_tag = []

                # Save to CSV
                writer.writerow({
                    "Tag": tag_name,
                    "Text": text,
                    "Author": author,
                    "About_link": about_link,
                    "Goodreads Page Link": goodreads_page_link,
                    "Inside Quote Tags": ", ".join(inside_tag)
                })

            # Pagination
            try:
                next_btn = driver.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
                next_btn.click()
            except:
                print(f"✅ Finished tag: {tag_name}")
                break

driver.quit()
