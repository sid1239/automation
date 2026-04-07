"""
Daily Leofame Instagram automation (Views + Likes + Saves + Shares)
- Runs all 4 services
- Waits 1 minute AFTER each click
- Takes screenshot immediately after click
- Takes another screenshot after 1 minute
- Sends both screenshots to Telegram

Requirements:
    pip install selenium webdriver-manager requests
"""

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URLS = [
    "https://leofame.com/free-instagram-views",
    "https://leofame.com/free-instagram-likes",
    "https://leofame.com/free-instagram-saves",
    "https://leofame.com/free-instagram-shares",
]

INSTAGRAM_LINK = "https://www.instagram.com/reel/DWwKjHqkkAm/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="
INTERVAL_SECONDS = 24 * 60 * 60

# ADD YOUR DETAILS HERE
TELEGRAM_BOT_TOKEN = "8793923431:AAH5eX0CGpos4v6u1XEMO8LTLxPm-QcH3rA"
TELEGRAM_CHAT_ID = "1814769108"


def send_to_telegram(image_path, caption=""):
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        requests.post(
            api_url,
            data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption},
            files={"photo": img},
            timeout=60,
        )


def submit_all_services():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    try:
        wait = WebDriverWait(driver, 20)

        for url in URLS:
            print(f"Opening {url}")
            driver.get(url)

            link_box = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder*='instagram.com']")
                )
            )
            link_box.clear()
            link_box.send_keys(INSTAGRAM_LINK)

            button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Get free')]")
                )
            )
            button.click()
            print(f"Submitted successfully for: {url}")

            page_name = url.split("/")[-1]

            # screenshot immediately after click
            shot1 = f"{page_name}_after_click.png"
            driver.save_screenshot(shot1)
            send_to_telegram(shot1, f"{page_name} - immediately after click")

            # wait 1 minute after click
            time.sleep(60)

            # screenshot after 1 minute
            shot2 = f"{page_name}_after_1min.png"
            driver.save_screenshot(shot2)
            send_to_telegram(shot2, f"{page_name} - after 1 minute")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    submit_all_services()
