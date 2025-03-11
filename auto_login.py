# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00467CA819E23E94BA43946C8DD3705813071B22F7D0249F1F28D0740801E071F3F9C658E64B66F4033FEA76D7728865F55199C6D96A97E1DB37040CC20439F5F50D3CD6D949B6382FE104129C06B1CF6F0946A311DDBCCB433D42BEF12919995CFDD8E4F799710FAAA18C0985866C8A383194DD0FDFAAFC0B297DD7DA41D5E01A80C29B1D102BADA6F56D45B4491B369B32E5F57A42F8E61BC38ECC8EB8C246F96F5E0D64D52442FA1C6F60C8A5967B565DBE352F9FB12143ADA05A9DDA95EC9A9F314CD3C64A6FB9494F1CFB9D5844895C6FD790F3C14D2430FC0DD7DA58B3D5FB882C1DB6537A98E2911A34A4E5CF5D02C43672F974EC951D3B8EA1BF196E7324248FC1280775C33AC691B97EE4DB695F24C35FE8FD46D4E138709B9ECD89A8AE7A9486A359718624D9A63E826F31EE7BC2F2D2B289E05492E778EA216B1B851B772DF7A4AADE3762E9E80544F4B091C8D5BD08FE8A28A0A12189E12FFBE736"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
