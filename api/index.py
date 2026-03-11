import asyncio
from flask import Flask, request
import requests

app = Flask(__name__)

# ይህንን ቶከን በድጋሚ አረጋግጥ
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    return requests.post(url, json=payload)

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def handler(path):
    if request.method == 'POST':
        data = request.get_json()
        
        # ቴሌግራም መልእክት ሲልክ እዚህ ጋር መረጃውን እናወጣለን
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_message = data["message"].get("text", "")

            if user_message == "/start":
                send_telegram_message(chat_id, "<b>ሰላም!</b> ቦቱ በትክክል እየሰራ ነው።\nእንኳን ደስ አለዎት!")
            else:
                send_telegram_message(chat_id, f"የላኩት መልእክት፡ <i>{user_message}</i>")
        
        return "OK", 200
    
    return "<h1>Bot Server is Live!</h1>"
