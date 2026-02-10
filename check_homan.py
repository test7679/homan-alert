import os
import requests
from playwright.sync_api import sync_playwright

# ===============================
# READ FROM GITHUB SECRETS
# ===============================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise RuntimeError("BOT_TOKEN or CHAT_ID not found in environment variables")

def send_alert(message: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, data=payload, timeout=30)
    response.raise_for_status()


def check_divyanugraha_homam():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("Opening TTD website...")

        page.goto(
            "https://ttdevasthanams.ap.gov.in/arjitha-seva/slot-booking",
            timeout=90_000
        )

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(5000)

        page_text = page.content().lower()

        if "divyanugraha" in page_text:
            send_alert(
                "🙏🙏🙏 TTD ALERT 🙏🙏🙏\n\n"
                "Divyanugraha Homam page has an update.\n"
                "Please check immediately:\n"
                "https://ttdevasthanams.ap.gov.in/arjitha-seva/slot-booking"
            )
        else:
            print("No update today.")

        browser.close()


if __name__ == "__main__":
    try:
        check_divyanugraha_homam()
    except Exception as e:
        send_alert(f"❌ TTD BOT ERROR:\n{str(e)}")
        raise
