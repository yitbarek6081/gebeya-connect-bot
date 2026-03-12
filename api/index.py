from flask import Flask, request
import urllib.request
import json

app = Flask(__name__)

# --- CONFIGURATION ---
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
ADMIN_ID = "7956330391"  # ያንተ የቴሌግራም ID (መረጃዎች ወደዚህ ይላካሉ)

# የላክኸው ፕሮፌሽናል HTML እዚህ ተቀምጧል
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ገበያ ኮኔክት - Gebeya Connect | የእርስዎ ዲጂታል የገበያ መድረክ</title>
    <link rel="icon" href="https://telegram.org/img/website_icon.svg" type="image/svg+xml">
    <style>
        :root { --primary-color: #0088cc; --secondary-color: #005588; --text-color: #333; --bg-color: #f4f7f6; }
        body { font-family: 'Segoe UI', Roboto, sans-serif; background: var(--bg-color); margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; color: var(--text-color); }
        .bg-gradient { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%); z-index: -1; clip-path: ellipse(150% 100% at 50% -50%); }
        .main-card { background: white; padding: 50px 40px; border-radius: 25px; box-shadow: 0 20px 50px rgba(0,0,0,0.15); text-align: center; max-width: 450px; width: 90%; position: relative; overflow: hidden; }
        .logo { font-size: 3rem; margin-bottom: 10px; }
        h1 { color: var(--secondary-color); font-size: 2.2rem; margin: 0 0 10px 0; }
        .slogan { font-size: 1.1rem; color: #666; margin-bottom: 30px; }
        .features { text-align: left; margin-bottom: 35px; background: #f9f9f9; padding: 20px; border-radius: 15px; border-left: 5px solid var(--primary-color); }
        .feature-item { display: flex; align-items: center; margin-bottom: 12px; }
        .feature-icon { color: var(--primary-color); margin-right: 10px; font-weight: bold; }
        .tg-btn { background: var(--primary-color); color: white; padding: 18px 35px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 1.2rem; display: flex; align-items: center; justify-content: center; transition: 0.3s; box-shadow: 0 10px 20px rgba(0,136,204,0.3); }
        .tg-btn:hover { background: var(--secondary-color); transform: translateY(-3px); }
        .tg-icon { width: 25px; height: 25px; margin-right: 12px; }
        .footer { margin-top: 40px; font-size: 0.9rem; color: rgba(255,255,255,0.8); }
    </style>
</head>
<body>
    <div class="bg-gradient"></div>
    <div class="main-card">
        <div class="logo">🛍️</div>
        <h1>ገበያ ኮኔክት</h1>
        <p class="slogan">የእርስዎ አስተማማኝ የዲጂታል ገበያ መድረክ በቴሌግራም። በቀላሉ ይግዙ፣ ይሽጡ፣ ይከራዩ!</p>
        <div class="features">
            <div class="feature-item"><span class="feature-icon">✓</span> መሬት፣ ቤት እና መኪና</div>
            <div class="feature-item"><span class="feature-icon">✓</span> ኤሌክትሮኒክስ እና ልዩ ልዩ ዕቃዎች</div>
            <div class="feature-item"><span class="feature-icon">✓</span> ፈጣን የመመዝገቢያ ሂደት</div>
        </div>
        <a href="https://t.me/yite_gebeyaconnect_bot" class="tg-btn">ወደ ቴሌግራም ቦቱ ሂድ</a>
    </div>
    <div class="footer">© 2026 Gebeya Connect | All rights reserved.</div>
</body>
</html>
"""

def send_msg(chat_id, text, reply_markup=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
    if reply_markup: payload["reply_markup"] = reply_markup
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

@app.route('/')
def home():
    return HTML_CONTENT

@app.route('/api/index', methods=['POST', 'GET'])
def handler():
    if request.method == 'POST':
        data = request.get_json()
        if "message" in data:
            chat_id = str(data["message"]["chat"]["id"])
            text = data["message"].get("text", "")

            # ዋና ማውጫ
            if text == "/start" or text == "🔙 ወደ ዋና ማውጫ":
                markup = {"keyboard": [[{"text": "➕ ዕቃ መመዝገብ"}, {"text": "🛍 የገበያ ዕቃ ዝርዝር"}]], "resize_keyboard": True}
                send_msg(chat_id, "<b>እንኳን ወደ ገበያ ኮኔክት በሰላም መጡ!</b>\nምን ማድረግ ይፈልጋሉ?", markup)

            # የዕቃ አይነት መምረጫ
            elif text == "➕ ዕቃ መመዝገብ":
                markup = {"keyboard": [[{"text": "🏘 መሬት"}, {"text": "🏠 ቤት"}], [{"text": "🚗 መኪና"}, {"text": "🏗 ኤሌክትሮኒክስ"}], [{"text": "🔙 ወደ ዋና ማውጫ"}]], "resize_keyboard": True}
                send_msg(chat_id, "የሚመዘገበውን የዕቃ አይነት ይምረጡ፡", markup)

            # ዝርዝር መመሪያዎች
            elif text in ["🏘 መሬት", "🏠 ቤት", "🚗 መኪና", "🏗 ኤሌክትሮኒክስ"]:
                send_msg(chat_id, f"<b>ደስ የሚል ምርጫ!</b>\n\nእባክዎ ስለ <b>{text}</b> መረጃውን (ቦታ፣ ስፋት፣ ዋጋ እና ስልክ) በአንድ መልእክት ይላኩ። ሻጮች ጋር እናገናኝዎታለን።")

            # ሌሎች መልእክቶች ወደ Admin እንዲተላለፉ
            elif chat_id != ADMIN_ID:
                send_msg(ADMIN_ID, f"<b>አዲስ መረጃ ደርሷል!</b>\nከ፡ @{data['message']['chat'].get('username', 'NoUsername')}\nID: {chat_id}\n\n{text}")
                send_msg(chat_id, "መረጃው ደርሶናል። እናመሰግናለን!")

        return "OK", 200
    return "Active", 200
