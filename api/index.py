from flask import Flask, request
import urllib.request
import json
import os

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "7956330391"
VERCEL_URL = "https://yite-gebeyaconnect.vercel.app/"

def send_msg(chat_id, text, markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if markup: payload["reply_markup"] = markup
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    return urllib.request.urlopen(req)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['POST', 'GET'])
def catch_all(path):
    if request.method == 'POST':
        update = request.get_json()
        if not update or "message" not in update:
            return "OK", 200
            
        chat_id = str(update["message"]["chat"]["id"])
        text = update["message"].get("text", "")

        # ዋና ማውጫ (Sketch ባደረግከው መሰረት)
        if text == "/start" or text == "🔙 ወደ ዋና ማውጫ":
            markup = {
                "keyboard": [
                    [{"text": "➕ ዕቃ መመዝገብ"}, {"text": "🛍 የገበያ ዕቃ ዝርዝር", "web_app": {"url": VERCEL_URL}}]
                ],
                "resize_keyboard": True
            }
            send_msg(chat_id, "<b>እንኳን ወደ ገበያ ኮኔክት በሰላም መጡ!</b>\n\nምን ማድረግ ይፈልጋሉ?", markup)

        # ዕቃ መመዝገቢያ አይነቶች
        elif text == "➕ ዕቃ መመዝገብ":
            markup = {
                "keyboard": [
                    [{"text": "🏘 መሬት"}, {"text": "🏠 ቤት"}],
                    [{"text": "🚗 መኪና"}, {"text": "🏗 ኤሌክትሮኒክስ"}],
                    [{"text": "🔙 ወደ ዋና ማውጫ"}]
                ],
                "resize_keyboard": True
            }
            send_msg(chat_id, "የሚመዘገበውን የዕቃ አይነት ይምረጡ፡", markup)

        # ለተጠቃሚው ምላሽ መስጠት እና መረጃውን ለ Admin መላክ
        elif text in ["🏘 መሬት", "🏠 ቤት", "🚗 መኪና", "🏗 ኤሌክትሮኒክስ"]:
            send_msg(chat_id, f"<b>{text} ለመመዝገብ፡</b>\nእባክዎ መረጃውን (ቦታ፣ ስፋት፣ ዋጋ እና ስልክ) በአንድ መልእክት ይላኩ።")

        elif chat_id != ADMIN_ID:
            send_msg(ADMIN_ID, f"<b>አዲስ መረጃ ደርሷል!</b>\nከ፡ {chat_id}\n\n{text}")
            send_msg(chat_id, "መረጃው ደርሶናል። እናመሰግናለን!")

        return "OK", 200

    # GET ጥያቄ ሲመጣ index.html ፋይልን ያሳያል
    try:
        # በ Vercel ላይ ፋይሉ የሚገኝበትን መንገድ መፈለግ
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_dir, 'index.html')
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "Gebeya Connect API is Active."
