import os
import requests
from playwright.sync_api import sync_playwright


BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send_alert(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    response = requests.post(url, json=payload, timeout=20)
    response.raise_for_status()


def check_divyanugraha_homam():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(
            "https://ttdevasthanams.ap.gov.in/arjitha-seva/slot-booking",
            timeout=60000
        )

        page.wait_for_selector("text=Seva Slots", timeout=60000)

        available_slots = page.locator("button.available, div.available")

        if available_slots.count() > 0:
            for i in range(available_slots.count()):
                date_text = available_slots.nth(i).inner_text()
                send_alert(
                    f"🙏 Divyaanugraha Homam AVAILABLE on {date_text}\nBook immediately!"
                )
        else:
            print("No slots available")

        browser.close()


if __name__ == "__main__":
    try:

        check_divyanugraha_homam()

    except Exception as e:
        send_alert(f"❌ TTD BOT ERROR:\n{str(e)}")
        raise
