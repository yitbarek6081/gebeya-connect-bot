from flask import Flask, request
import urllib.request
import json
import os

app = Flask(__name__)

# --- ኮንፊገሬሽን ---
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "6348873724"
ADMIN_PHONE = "0945880474" # ያንተ ስልክ ቁጥር
VERCEL_URL = "https://yite-gebeyaconnect.vercel.app/"

CITIES = ["ወልድያ", "ኮቦ", "ሲሪንቃ", "መርሳ", "ዉርጌሳ", "ዉጫሌ", "ሃይቅ", "ደሴ", "ኮምቦልቻ"]

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
        if not update or "message" not in update: return "OK", 200
        
        chat_id = str(update["message"]["chat"]["id"])
        text = update["message"].get("text", "")

        # ዋና ማውጫ
        if text == "/start" or "ዋና ማውጫ" in text:
            markup = {
                "keyboard": [[{"text": "➕ ዕቃ መመዝገብ"}, {"text": "🛍 የገበያ ዕቃ ዝርዝር", "web_app": {"url": VERCEL_URL}}]],
                "resize_keyboard": True
            }
            send_msg(chat_id, "<b>እንኳን ወደ ገበያ ኮኔክት በሰላም መጡ!</b>\nምን ማድረግ ይፈልጋሉ?", markup)

        # 1ኛ ደረጃ፡ ዕቃ መመዝገብ ሲነካ
        elif text == "➕ ዕቃ መመዝገብ":
            markup = {
                "keyboard": [[{"text": "🏘 መሬት"}, {"text": "🏠 ቤት"}], [{"text": "🚗 መኪና"}, {"text": "🏗 ኤሌክትሮኒክስ"}], [{"text": "🔙 ወደ ዋና ማውጫ"}]],
                "resize_keyboard": True
            }
            send_msg(chat_id, "<b>የሚመዘገበውን የዕቃ አይነት ይምረጡ፡</b>", markup)

        # 2ኛ ደረጃ፡ ከተማ መምረጫ
        elif text in ["🏘 መሬት", "🏠 ቤት", "🚗 መኪና", "🏗 ኤሌክትሮኒክስ"]:
            # ከተማዎቹን ጎን ለጎን በ3 ረድፍ ማሳያ
            rows = []
            for i in range(0, len(CITIES), 3):
                rows.append([{"text": CITIES[i]}, {"text": CITIES[i+1]}, {"text": CITIES[i+2]}])
            markup = {"keyboard": rows, "resize_keyboard": True}
            send_msg(chat_id, f"📍 <b>ለ{text} የሚገኝበትን ከተማ ይምረጡ፡</b>", markup)

        # 3ኛ ደረጃ፡ የከተማ ምርጫ ከተጠናቀቀ በኋላ መመሪያ መስጠት
        elif text in CITIES:
            instruction = (
                f"✅ <b>ከተማ፦ {text} ተመርጧል</b>\n\n"
                "አሁን እባክዎን ቀሪዎቹን መረጃዎች በዚህ መልክ በአንድ መልዕክት ይላኩ፡\n"
                "1. 📍 <b>ልዩ ቦታ</b>\n"
                "2. 📏 <b>ስፋት</b> (ለመሬትና ቤት ብቻ)\n"
                "3. 💰 <b>ዋጋ</b>\n"
                "4. 📞 <b>ስልክ ቁጥርዎ</b>\n\n"
                "<i>ሁሉንም ጽፈው ሲጨርሱ 'Submit' ለማድረግ ይላኩት።</i>"
            )
            send_msg(chat_id, instruction)

        # 4ኛ ደረጃ፡ ሙሉ መረጃውን ለአድሚን መላክ (የሻጩ ስልክ ቁጥር እዚህ ይካተታል)
        elif chat_id != ADMIN_ID and text not in ["/start"] and "➕" not in text:
            # ለአድሚን የሚላክ
            admin_msg = f"<b>🚨 አዲስ ምዝገባ ደርሷል!</b>\n\n<b>ዝርዝር መረጃ፦</b>\n<code>{text}</code>\n\n<b>የሻጭ መለያ (ID):</b> {chat_id}"
            send_msg(ADMIN_ID, admin_msg)
            # ለተጠቃሚው ምላሽ
            send_msg(chat_id, "<b>✅ መረጃው በትክክል ተመዝግቧል። እናመሰግናለን!</b>")

        return "OK", 200

    # ለ Mini App (Web ገጽ)
    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "Gebeya Connect Live"
