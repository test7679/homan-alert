from playwright.sync_api import sync_playwright
import telegram

from telegram import Bot
Bot("8590808423:AAGfPUTWclH-pW-dM1H3ubk4Lu_SJMQnG8k").send_message(
    chat_id="8532019043",
    text="✅ TEST: TTD GitHub Action is running"
)

BOT_TOKEN = "8590808423:AAGfPUTWclH-pW-dM1H3ubk4Lu_SJMQnG8k"
CHAT_ID = "8532019043"

def send_alert(date_text):
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(
        chat_id=CHAT_ID,
        text=f"🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏🙏 Divyaanugraha Homam AVAILABLE on {date_text}. Book immediately!"
    )

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
            date = available_slots.nth(i).inner_text()
            send_alert(date)

    browser.close()
