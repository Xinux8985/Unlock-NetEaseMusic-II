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
    browser.add_cookie({"name": "MUSIC_U", "value": "00EDDE9030A81EB93C2ADF1998E3781714D3CCDAA959C92F1D8212C231E2A2F320F9D92169BFE7FCA0A2D48E2EEC7EEA05EA275F4EDAB4DD7EFA54788E8ECF5248CBE772C00093DD6E4FDC0BCDADF4867E6218A41EE656FE5E3EBAA4479A37301F6571BA7A469B1CB020E4CE6BFFD6B9325E13767B69AD25FF4AD1166485C1984C543E3B5E9CC456357C18ADC066C5AF049816331743AF336CBA335733ECE6D5DEC84D3C686D6E8C271C5F5E5F0ACF2F34572CB238B244AEA0E1508B06F0D8D62818E5B264887713D6F25B970822385FE14827FAAFD411430CA02BDDF458B3EC5C8B64F401C14A9A27C82FC0FE3C9984A300A9956B6D94178730947F5DE381C9751B9060D2CA385A2F6573783495BB0C9CF5AC58941B5D90FE3A7D50770281126991DCF88C1FAB38B3C6DA48DCA1106D32BE279ABD12006DA636A0314D0E1DDD6694FEB2FC7AFDD4DFFE8E475B5B4E608D6BC35E94A707980BBD1649A844D07D34"})
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
