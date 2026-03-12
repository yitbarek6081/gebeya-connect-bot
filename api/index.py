from flask import Flask, request
import urllib.request
import json
import os

app = Flask(__name__)

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "7956330391"
ADMIN_PHONE = "0945880474"
VERCEL_URL = "https://yite-gebeyaconnect.vercel.app/"

CITIES = ["ወልድያ", "ኮቦ", "ሲሪንቃ", "መርሳ", "ዉርጌሳ", "ዉጫሌ", "ሃይቅ", "ደሴ", "ኮምቦልቻ"]

# የተጠቃሚዎችን የዝግጅት ደረጃ ለመያዝ
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

        # 1. መጀመሪያ /start ወይም ዋና ማውጫ
        if text == "/start" or "ዋና ማውጫ" in text:
            user_states[chat_id] = {}
            markup = {
                "keyboard": [[{"text": "➕ ዕቃ መመዝገብ"}, {"text": "🛍 የገበያ ዕቃ ዝርዝር", "web_app": {"url": VERCEL_URL}}]],
                "resize_keyboard": True
            }
            send_msg(chat_id, "<b>እንኳን ወደ ገበያ ኮኔክት በሰላም መጡ!</b>", markup)

        # 2. ዕቃ መመዝገብ ሲነካ
        elif text == "➕ ዕቃ መመዝገብ":
            markup = {
                "keyboard": [[{"text": "🏘 መሬት"}, {"text": "🏠 ቤት"}], [{"text": "🚗 መኪና"}, {"text": "🏗 ኤሌክትሮኒክስ"}]],
                "resize_keyboard": True
            }
            send_msg(chat_id, "የሚመዘገበውን የዕቃ አይነት ይምረጡ፡", markup)

        # 3. የምድብ ምርጫ (መሬት/ቤት/መኪና/ኤሌክትሮኒክስ)
        elif text in ["🏘 መሬት", "🏠 ቤት", "🚗 መኪና", "🏗 ኤሌክትሮኒክስ"]:
            user_states[chat_id] = {"category": text, "step": "city"}
            city_btns = [[{"text": CITIES[i]}, {"text": CITIES[i+1]}, {"text": CITIES[i+2]}] for i in range(0, 9, 3)]
            markup = {"keyboard": city_btns, "resize_keyboard": True}
            send_msg(chat_id, f"📍 1ኛ፦ የ{text} የሚገኝበትን <b>ከተማ</b> ይምረጡ፡", markup)

        # 4. ደረጃ በደረጃ መረጃ መቀበል
        elif chat_id in user_states and "step" in user_states[chat_id]:
            state = user_states[chat_id]
            
            if state["step"] == "city" and text in CITIES:
                state["city"] = text
                state["step"] = "location"
                send_msg(chat_id, "📍 2ኛ፦ <b>ልዩ ቦታውን</b> በጽሁፍ ያስገቡ፡", {"remove_keyboard": True})
                
            elif state["step"] == "location":
                state["location"] = text
                if state["category"] in ["🏘 መሬት", "🏠 ቤት"]:
                    state["step"] = "area"
                    send_msg(chat_id, "📐 3ኛ፦ <b>ስፋት</b> ያስገቡ (ለምሳሌ፡ 200 ካሬ)፡")
                else:
                    state["step"] = "price"
                    send_msg(chat_id, "💰 3ኛ፦ <b>ዋጋ</b> ያስገቡ (ለምሳሌ፡ 500,000 ብር)፡")

            elif state["step"] == "area":
                state["area"] = text
                state["step"] = "price"
                send_msg(chat_id, "💰 4ኛ፦ <b>ዋጋ</b> ያስገቡ፡")

            elif state["step"] == "price":
                state["price"] = text
                state["step"] = "phone"
                send_msg(chat_id, "📞 5ኛ፦ <b>ስልክ ቁጥር</b> ያስገቡ፡")

            elif state["step"] == "phone":
                state["phone"] = text
                # ማጠቃለያ መረጃ ለአድሚን
                summary = (f"🔔 <b>አዲስ {state['category']} ምዝገባ!</b>\n\n"
                           f"📍 ከተማ: {state['city']}\n📍 ልዩ ቦታ: {state['location']}\n"
                           f"{'📐 ስፋት: ' + state.get('area', '') + ' ' if 'area' in state else ''}"
                           f"💰 ዋጋ: {state['price']}\n📞 ስልክ: {state['phone']}")
                
                send_msg(ADMIN_ID, summary)
                send_msg(chat_id, "<b>✅ ምዝገባው ተጠናቋል! መረጃው ተልኳል።</b>")
                del user_states[chat_id] # State ማጽዳት

        return "OK", 200

    with open('index.html', 'r', encoding='utf-8') as f: return f.read()
