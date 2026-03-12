from flask import Flask, request
import urllib.request
import json
import os

app = Flask(__name__)

# --- CONFIG ---
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "7956330391"
# የ Google Sheet ስክሪፕት ሊንክ እዚህ ይገባል (ከታች ያለውን መመሪያ ተከተል)
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

        # (ከላይ የነበረው የደረጃ በደረጃ ምዝገባ አመክንዮ እዚህ ይቀጥላል...)
        # ...

        # 5ኛ ደረጃ ላይ ስልክ ሲገባ መረጃውን ወደ Sheet መላክ
        if chat_id in user_states and user_states[chat_id].get("step") == "phone":
            state = user_states[chat_id]
            state["phone"] = text
            
            # ወደ Google Sheet መላክ
            sheet_data = {
                "category": state["category"],
                "city": state["city"],
                "location": state["location"],
                "area": state.get("area", "-"),
                "price": state["price"],
                "phone": state["phone"]
            }
            
            # መረጃውን ወደ Sheet Script መላክ
            req = urllib.request.Request(SHEET_SCRIPT_URL, data=json.dumps(sheet_data).encode('utf-8'))
            try: urllib.request.urlopen(req)
            except: pass

            send_msg(ADMIN_ID, f"🚨 አዲስ ምዝገባ!\n{state['category']} - {state['city']}")
            send_msg(chat_id, "<b>✅ መረጃው በገበያ ዝርዝር ላይ ተመዝግቧል። እናመሰግናለን!</b>")
            del user_states[chat_id]

        return "OK", 200
    
    # ለገበያ ዝርዝሩ (GET)
    return "Marketplace active"
