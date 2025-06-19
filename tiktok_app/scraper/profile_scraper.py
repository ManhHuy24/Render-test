# scraper/profile_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time, random
from datetime import datetime
from tiktok_captcha_solver import make_undetected_chromedriver_solver
from selenium_stealth import stealth
import undetected_chromedriver as uc
import chromedriver_autoinstaller

def scrape_profiles(input_file, output_file):
    chromedriver_autoinstaller.install()
    # service = Service("chromedriver.exe")
    # api_key = "5fe871299e9a4e80267ba952e4b8df24"
    # options = uc.ChromeOptions()
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-infobars")
    options.add_argument("--window-size=1920,1080")

    # driver = make_undetected_chromedriver_solver(api_key, options=options)

    driver = webdriver.Chrome(options=options)
    df = pd.read_csv(input_file)
    results = []

    for index, row in df.iterrows():
        url = row['Profile URL']
        print(f"[{index+1}/{len(df)}] {url}")
        try:
            driver.get(url)
            time.sleep(random.uniform(3, 5))
            stats = {
                'Following': driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="following-count"]').text,
                'Followers': driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="followers-count"]').text,
                'Likes': driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="likes-count"]').text,
                'Bio': driver.find_element(By.CSS_SELECTOR, 'h2[data-e2e="user-bio"]').text,
            }
            results.append({**row.to_dict(), **stats})
        except NoSuchElementException:
            print("Không tìm thấy thông tin.")
        time.sleep(random.uniform(2, 4))

    driver.quit()
    pd.DataFrame(results).to_csv(output_file, index=False, encoding='utf-8-sig')
