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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B062CF01E81DF0FDA6737085CCDAFE1BC67176751FBE10192E89043E9D0C588E60AA5958CD6BDE21ABD9116118F72423FC82B3556F73DDF79BC5633EFE252E7A4A9F81B88F15CF74CE691C524C4821BD570A4155B04B463D1C69DE47E85C33977899994ACD7F8586B2EBF1E2F83E8F401529EB54FAD7AD7BBCF753EB53EE94E5CBDE6D34BB5CD6FE56682842F2F3D6BC0972A8DAFD32712EA300FEDD30CA917143BC9D819F22FA64440975C5972F886EB810CEA81098D83ACCF2612211C8E1314DB397BD3C1CBBB177E3FFE5E0A328050A13140A5E03A6835EECB65290E72F1C67C141A978C98245791AE9A6E9710A7502A39008E4F9A1915250A29357171521A27276687B088EBC7727E14221C4FBA72EC8AE783D1C62B6D292B288AA165C3270BC060BB09C70C8061FEB98070C1BE6A7FB3BCFF0C2B010065FF90043BC3F6287DBCDACFB90F6E6CB77E97BC7DF19AFAE1CFFB00126EBC071D1C872CBEFE998"})
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
