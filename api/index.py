from flask import Flask, request, render_template_string
import urllib.request
import json
import os

app = Flask(__name__)

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"

@app.route('/')
def home():
    # index.html ፋይሉን አንብቦ ለብራውዘር ይልካል
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "<h1>Gebeya Connect is Live!</h1><p>Visit us on Telegram.</p>"

@app.route('/api/index', methods=['POST', 'GET'])
def telegram_webhook():
    if request.method == 'POST':
        data = request.get_json()
        if data and "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "")
            
            # የቦቱ ቁልፎች (Buttons)
            reply_markup = {
                "keyboard": [
                    [{"text": "🛍 ዕቃዎችን እይ"}, {"text": "➕ ዕቃ መዝግብ"}],
                    [{"text": "📞 እኛን ለማግኘት"}]
                ],
                "resize_keyboard": True
            }

            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": chat_id, 
                "text": "እንኳን ወደ ገበያ ኮኔክት መጡ! ምን ላግዝዎት?",
                "reply_markup": reply_markup
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
            
        return "OK", 200
    return "Webhook is active!", 200
