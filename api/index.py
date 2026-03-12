from flask import Flask, request
import urllib.request
import json
import os

app = Flask(__name__)

# --- CONFIG ---
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "7956330391"
ADMIN_PHONE = "0945880474"
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
            send_msg(chat_id, "<b>እንኳን ወደ 🛍 ገበያ ኮኔክት በሰላም መጡ!</b>\n\nምን ማድረግ ይፈልጋሉ?", markup)

        # 1. ዕቃ መመዝገብ
        elif text == "➕ ዕቃ መመዝገብ":
            markup = {
                "keyboard": [[{"text": "🏘 መሬት"}, {"text": "🏠 ቤት"}], [{"text": "🚗 መኪና"}, {"text": "🏗 ኤሌክትሮኒክስ"}], [{"text": "🔙 ወደ ዋና ማውጫ"}]],
                "resize_keyboard": True
            }
            send_msg(chat_id, "<b>የሚመዘገበውን የዕቃ አይነት ይምረጡ፡</b>", markup)

        # 2. ከተማ መምረጫ (ለአራቱም ምድቦች)
        elif text in ["🏘 መሬት", "🏠 ቤት", "🚗 መኪና", "🏗 ኤሌክትሮኒክስ"]:
            rows = []
            for i in range(0, len(CITIES), 3):
                rows.append([{"text": CITIES[i]}, {"text": CITIES[i+1]}, {"text": CITIES[i+2]}])
            markup = {"keyboard": rows, "resize_keyboard": True}
            send_msg(chat_id, f"📍 <b>ለ{text} የሚገኝበትን ከተማ ይምረጡ፡</b>", markup)

        # 3. ቀሪ መረጃዎችን መቀበያ
        elif text in CITIES:
            # እዚህ ጋር ተጠቃሚው ቀሪዎቹን 4 ወይም 3 መረጃዎች እንዲልክ እናዝዘዋለን
            msg = (
                f"✅ <b>ከተማ፦ {text} ተመርጧል</b>\n\n"
                "አሁን እባክዎን ቀሪዎቹን መረጃዎች በቅደም ተከተል በአንድ መልእክት ይላኩ፡\n"
                "1. 📍 ልዩ ቦታ\n"
                "2. 📏 ስፋት (ለመሬትና ቤት ብቻ)\n"
                "3. 💰 ዋጋ\n"
                "4. 📞 ስልክ\n\n"
                "<i>ሁሉንም ጽፈው ሲጨርሱ 'Submit' ለማድረግ ይላኩት።</i>"
            )
            send_msg(chat_id, msg)

        # 4. መረጃውን ለ Admin መላክ (የሻጭ ስልክ ቁጥር እዚህ ይታያል)
        elif chat_id != ADMIN_ID and text not in ["/start"] and "➕" not in text:
            # ለአድሚን የሚላክ
            send_msg(ADMIN_ID, f"<b>🚨 አዲስ ምዝገባ!</b>\nከ፡ {chat_id}\n\n<b>መረጃ፦</b>\n{text}")
            # ለተጠቃሚው ምላሽ
            send_msg(chat_id, "<b>✅ መረጃው በትክክል ተመዝግቧል። እናመሰግናለን!</b>")

        return "OK", 200

    try:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(base_dir, 'index.html'), 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "Gebeya Connect Live"
