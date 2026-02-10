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

        # Let calendar JS fully render
        page.wait_for_timeout(6000)

        green_dates = []

        # Calendar date buttons
        date_buttons = page.locator("td button")

        for i in range(date_buttons.count()):
            btn = date_buttons.nth(i)

            bg_color = btn.evaluate(
                "el => window.getComputedStyle(el).backgroundColor"
            )

            date_text = btn.inner_text().strip()

            # 🔍 DEBUG (REMOVE LATER)
            print(date_text, bg_color)

            # Detect ANY shade of green safely
            if bg_color.startswith("rgb"):
                r, g, b = map(
                    int,
                    bg_color.replace("rgb(", "").replace(")", "").split(",")
                )

                if g > 100 and r < 120 and b < 120 and date_text:
                    green_dates.append(date_text)

        if green_dates:
            send_alert(
                "🟢 Divyanugraha Homam AVAILABLE!\n\n"
                "Available dates:\n"
                + ", ".join(green_dates) +
                "\n\n👉 Book immediately:\n"
                "https://ttdevasthanams.ap.gov.in"
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
