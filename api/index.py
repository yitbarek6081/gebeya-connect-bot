from flask import Flask, request, jsonify
import urllib.request
import json
import os

app = Flask(__name__)

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "7956330391"
# እዚህ ጋር የ Google Script ሊንክህን አስገባ
SHEET_SCRIPT_URL = "የእርስዎ_የስክሪፕት_ሊንክ_እዚህ" 

CITIES = ["ወልድያ", "ኮቦ", "ሲሪንቃ", "መርሳ", "ዉርጌሳ", "ዉጫሌ", "ሃይቅ", "ደሴ", "ኮምቦልቻ"]
user_states = {}

def send_msg(chat_id, text, markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if markup: payload["reply_markup"] = markup
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try: urllib.request.urlopen(req)
    except: pass

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        update = request.get_json()
        if not update or "message" not in update: return "OK", 200
        chat_id = str(update["message"]["chat"]["id"])
        text = update["message"].get("text", "")

        if text == "/start" or "ዋና ማውጫ" in text:
            user_states[chat_id] = {}
            markup = {"keyboard": [[{"text": "➕ ዕቃ መመዝገብ"}, {"text": "🛍 የገበያ ዕቃ ዝርዝር", "web_app": {"url": request.host_url}}]], "resize_keyboard": True}
            send_msg(chat_id, "<b>እንኳን ወደ ገበያ ኮኔክት በሰላም መጡ!</b>", markup)

        elif text == "➕ ዕቃ መመዝገብ":
            markup = {"keyboard": [[{"text": "🏘 መሬት"}, {"text": "🏠 ቤት"}], [{"text": "🚗 መኪና"}, {"text": "🏗 ኤሌክትሮኒክስ"}]], "resize_keyboard": True}
            send_msg(chat_id, "የሚመዘገበውን የዕቃ አይነት ይምረጡ፡", markup)

        elif text in ["🏘 መሬት", "🏠 ቤት", "🚗 መኪና", "🏗 ኤሌክትሮኒክስ"]:
            user_states[chat_id] = {"category": text, "step": "city"}
            city_btns = [[{"text": CITIES[i]}, {"text": CITIES[i+1]}, {"text": CITIES[i+2]}] for i in range(0, 9, 3)]
            send_msg(chat_id, f"📍 1ኛ፦ የ{text} የሚገኝበትን ከተማ ይምረጡ፡", {"keyboard": city_btns, "resize_keyboard": True})

        elif chat_id in user_states and "step" in user_states[chat_id]:
            state = user_states[chat_id]
            if state["step"] == "city":
                state["city"], state["step"] = text, "location"
                send_msg(chat_id, "📍 2ኛ፦ ልዩ ቦታውን ያስገቡ፡", {"remove_keyboard": True})
            elif state["step"] == "location":
                state["location"] = text
                state["step"] = "area" if state["category"] in ["🏘 መሬት", "🏠 ቤት"] else "price"
                send_msg(chat_id, "📐 3ኛ፦ ስፋት ያስገቡ፡" if state["step"] == "area" else "💰 3ኛ፦ ዋጋ ያስገቡ፡")
            elif state["step"] == "area":
                state["area"], state["step"] = text, "price"
                send_msg(chat_id, "💰 4ኛ፦ ዋጋ ያስገቡ፡")
            elif state["step"] == "price":
                state["price"], state["step"] = text, "phone"
                send_msg(chat_id, "📞 5ኛ፦ ስልክ ቁጥር ያስገቡ፡")
            elif state["step"] == "phone":
                state["phone"] = text
                # ወደ Sheet መላክ
                sheet_payload = {"category": state["category"], "city": state["city"], "location": state["location"], "area": state.get("area", "-"), "price": state["price"], "phone": state["phone"]}
                req = urllib.request.Request(SHEET_SCRIPT_URL, data=json.dumps(sheet_payload).encode('utf-8'), method='POST')
                try: urllib.request.urlopen(req)
                except: pass
                send_msg(chat_id, "<b>✅ ምዝገባው ተሳክቷል! ገበያው ላይ ይታያል።</b>")
                del user_states[chat_id]
        return "OK", 200

    # ለገበያ ዝርዝሩ (GET)
    try:
        with open('index.html', 'r', encoding='utf-8') as f: return f.read()
    except: return "Index file missing"
