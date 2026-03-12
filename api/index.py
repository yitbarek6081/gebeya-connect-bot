from flask import Flask, request
import urllib.request
import json

app = Flask(__name__)

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "7956330391"

# የላክኸው ፕሮፌሽናል HTML ገጽ
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ገበያ ኮኔክት - Gebeya Connect</title>
    <style>
        :root { --primary-color: #0088cc; --secondary-color: #005588; --bg-color: #f4f7f6; }
        body { font-family: 'Segoe UI', Roboto, sans-serif; background: var(--bg-color); margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; }
        .bg-gradient { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); z-index: -1; clip-path: ellipse(150% 100% at 50% -50%); }
        .main-card { background: white; padding: 50px 40px; border-radius: 25px; box-shadow: 0 20px 50px rgba(0,0,0,0.15); text-align: center; max-width: 450px; width: 90%; }
        h1 { color: var(--secondary-color); font-size: 2.2rem; margin: 10px 0; }
        .features { text-align: left; margin: 20px 0; background: #f9f9f9; padding: 15px; border-radius: 15px; border-left: 5px solid var(--primary-color); }
        .tg-btn { background: var(--primary-color); color: white; padding: 18px 30px; text-decoration: none; border-radius: 50px; font-weight: bold; display: flex; align-items: center; justify-content: center; transition: 0.3s; box-shadow: 0 10px 20px rgba(0,136,204,0.3); }
        .tg-btn:hover { background: var(--secondary-color); transform: translateY(-3px); }
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <div class="main-card">
        <div style="font-size: 3rem;">🛍️</div>
        <h1>ገበያ ኮኔክት</h1>
        <p>በቀላሉ ይግዙ፣ ይሽጡ፣ ይከራዩ!</p>
        <div class="features">
            <div>✓ መሬት፣ ቤት እና መኪና</div>
            <div>✓ ኤሌክትሮኒክስ እና ልዩ ልዩ ዕቃዎች</div>
        </div>
        <a href="https://t.me/yite_gebeyaconnect_bot" class="tg-btn">ወደ ቴሌግራም ቦቱ ሂድ</a>
    </div>
</body>
</html>
"""

def send_msg(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup: payload["reply_markup"] = reply_markup
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['POST', 'GET'])
def catch_all(path):
    if request.method == 'POST':
        data = request.get_json()
        if data and "message" in data:
            chat_id = str(data["message"]["chat"]["id"])
            text = data["message"].get("text", "")

            if text == "/start" or text == "🔙 ወደ ዋና ማውጫ":
                markup = {"keyboard": [[{"text": "➕ ዕቃ መመዝገብ"}, {"text": "🛍 የገበያ ዕቃ ዝርዝር"}]], "resize_keyboard": True}
                send_msg(chat_id, "<b>እንኳን ወደ ገበያ ኮኔክት በሰላም መጡ!</b>", markup)
            
            elif text == "➕ ዕቃ መመዝገብ":
                markup = {"keyboard": [[{"text": "🏘 መሬት"}, {"text": "🏠 ቤት"}], [{"text": "🚗 መኪና"}, {"text": "🏗 ኤሌክትሮኒክስ"}], [{"text": "🔙 ወደ ዋና ማውጫ"}]], "resize_keyboard": True}
                send_msg(chat_id, "የሚመዘገበውን የዕቃ አይነት ይምረጡ፡", markup)
            
            elif text in ["🏘 መሬት", "🏠 ቤት", "🚗 መኪና", "🏗 ኤሌክትሮኒክስ"]:
                send_msg(chat_id, f"<b>{text}</b> ለመመዝገብ መረጃውን (ቦታ፣ ስፋት፣ ዋጋ እና ስልክ) ይላኩ።")
            
            elif chat_id != ADMIN_ID:
                send_msg(ADMIN_ID, f"<b>አዲስ መረጃ፡</b>\nID: {chat_id}\n\n{text}")
                send_msg(chat_id, "መረጃው ደርሶናል። እናመሰግናለን!")

        return "OK", 200
    
    return HTML_CONTENT
