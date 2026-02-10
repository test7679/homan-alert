import os
import requests
from playwright.sync_api import sync_playwright

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_alert(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    r = requests.post(url, json=payload, timeout=20)
    r.raise_for_status()


def check_divyanugraha_homam():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(
            "https://ttdevasthanams.ap.gov.in/arjitha-seva/slot-booking",
            wait_until="networkidle",
            timeout=90000
        )

        # Allow calendar JS to fully render
        page.wait_for_timeout(6000)

        # 🔍 GREEN DATE DETECTION (robust)
        green_dates = page.locator(
            "button:enabled, "
            "td[style*='green'], "
            "td.available, "
            "button.available"
        )

        green_count = green_dates.count()

        if green_count > 0:
            send_alert(
                f"🟢 Divyanugraha Homam slots OPEN!\n"
                f"Available dates found: {green_count}\n\n"
                f"👉 Book immediately:\n"
                f"https://ttdevasthanams.ap.gov.in"
            )
        else:
            print("No green dates available")

        browser.close()


if __name__ == "__main__":
    try:
        check_divyanugraha_homam()
    except Exception as e:
        send_alert(f"❌ TTD BOT ERROR:\n{str(e)}")
        raise
