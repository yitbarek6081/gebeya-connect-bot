from flask import Flask, request
import urllib.request
import json

app = Flask(__name__)

# --- መረጃዎች ---
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "7956330391"

# ፕሮፌሽናል HTML ገጽ
HTML_PAGE = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ገበያ ኮኔክት - Gebeya Connect</title>
    <style>
        :root { --primary: #0088cc; --dark: #005588; }
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; margin: 0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
        .bg { position: fixed; top: 0; width: 100%; height: 100%; background: linear-gradient(135deg, var(--primary) 0%, var(--dark) 100%); z-index: -1; clip-path: ellipse(150% 100% at 50% -50%); }
        .card { background: white; padding: 50px 30px; border-radius: 25px; box-shadow: 0 15px 40px rgba(0,0,0,0.15); text-align: center; max-width: 400px; width: 90%; }
        h1 { color: var(--dark); margin: 10px 0; }
        .tg-btn { background: var(--primary); color: white; padding: 18px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; display: block; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="bg"></div>
    <div class="card">
        <div style="font-size: 3rem;">🛍️</div>
        <h1>ገበያ ኮኔክት</h1>
        <p>በቀላሉ ይግዙ፣ ይሽጡ፣ ይከራዩ!</p>
        <a href="https://t.me/yite_gebeyaconnect_bot" class="tg-btn">ወደ ቴሌግራም ቦቱ ሂድ</a>
    </div>
</body>
</html>
"""

def send_msg(chat_id, text, markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if markup: data["reply_markup"] = markup
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
    return urllib.request.urlopen(req)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        update = request.get_json()
        if "message" in update:
            chat_id = str(update["message"]["chat"]["id"])
            text = update["message"].get("text", "")

            # ዋና ማውጫ
            if text == "/start" or text == "🔙 ወደ ዋና ማውጫ":
                markup = {"keyboard": [[{"text": "➕ ዕቃ መመዝገብ"}, {"text": "🛍 የገበያ ዕቃ ዝርዝር"}]], "resize_keyboard": True}
                send_msg(chat_id, "<b>እንኳን ወደ ገበያ ኮኔክት በሰላም መጡ!</b>\n\nምን ማድረግ ይፈልጋሉ?", markup)

            # የመመዝገቢያ አይነቶች
            elif text == "➕ ዕቃ መመዝገብ":
                markup = {"keyboard": [[{"text": "🏘 መሬት"}, {"text": "🏠 ቤት"}], [{"text": "🚗 መኪና"}, {"text": "🏗 ኤሌክትሮኒክስ"}], [{"text": "🔙 ወደ ዋና ማውጫ"}]], "resize_keyboard": True}
                send_msg(chat_id, "የሚመዘገበውን የዕቃ አይነት ይምረጡ፡", markup)

            # ለእያንዳንዱ አይነት ምላሽ
            elif text in ["🏘 መሬት", "🏠 ቤት", "🚗 መኪና", "🏗 ኤሌክትሮኒክስ"]:
                send_msg(chat_id, f"<b>{text} ለመመዝገብ፡</b>\nእባክዎ መረጃውን (ቦታ፣ ስፋት፣ ዋጋ እና ስልክ) በአንድ መልእክት ይላኩ።")

            # መረጃን ወደ Admin ማስተላለፍ
            elif chat_id != ADMIN_ID:
                send_msg(ADMIN_ID, f"<b>አዲስ መረጃ ደርሷል!</b>\nከ፡ {chat_id}\n\n{text}")
                send_msg(chat_id, "መረጃው ደርሶናል። እናመሰግናለን!")

        return "OK", 200
    
    return HTML_PAGE
