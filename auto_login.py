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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E310A5A9B5BD1167077E0BE260A65151F5E0EFB6669DC1C155FDCD17BAADCE16E4A9DB4272599931C67BD19F99D46631C8B2C316166C4A4D95C4CEEA41B9601A851449257D1561B1FB5A7CF67460359DF0D943CE1681EA1CC9D3553F0C8540C3ABADB5FDB976C5505050E65AAAFEFB60C875FFCD5CE63BB37A0D1BFDB37CF3EBF2C03651258098F47FEC13220B904DEF6A3A31ED3915EE36D5AC66350545FB56289EC53B2A4363DF38A42E861290C0080C1CCFF52FFAC37F126ED3B7227F292D715CFAB7D5C04E999C58C2C5C93E14DBBF5DB49F2C7D6033D77E8F2FF0DC93923CB031ED357D8173B6281F7B4AEB20610FFBDBDB818E61665F9853FBE8743B61EDBE4DDA9078110267F8B3A980FDF66028B99F6D28F762AB8131A753D6F52487BFA10080CD3015096D578482C983DF76C05FDD07D1D7EE94E14DA501A6EB5FDC20D6D899D1E3DCAC1AC49F011A6355C964BFCCE28AB61B372DE7995921C381F8"})
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
