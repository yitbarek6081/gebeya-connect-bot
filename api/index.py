from flask import Flask, request
import urllib.request
import json

# ይህ ስም 'app' መሆኑ በጣም ወሳኝ ነው
app = Flask(__name__)

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"

@app.route('/')
def home():
    return "Bot Server is Running!"

@app.route('/api/index', methods=['POST', 'GET'])
def telegram_webhook():
    if request.method == 'POST':
        data = request.get_json()
        if data and "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "")
            
            # መልእክት መላኪያ
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": chat_id, 
                "text": f"በመጨረሻ ሰርቷል! የላከው መልእክት፡ {user_text}"
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
            
        return "OK", 200
    return "Webhook is active!", 200

# ይህን መስመር መጨረሻ ላይ ጨምረው
app.debug = True
