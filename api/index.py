from flask import Flask, request
import requests

app = Flask(__name__)

# የቦት ቶከንህ
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {
            "keyboard": [
                [{"text": "🛍 ዕቃዎችን እይ"}, {"text": "➕ ዕቃ መዝግብ"}],
                [{"text": "📞 እኛን ለማግኘት"}]
            ],
            "resize_keyboard": True
        }
    }
    return requests.post(url, json=payload)

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def handler(path):
    if request.method == 'POST':
        data = request.get_json()
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "")

            if user_text == "/start":
                send_message(chat_id, "<b>ሰላም! እንኳን ወደ ገበያ ኮኔክት በሰላም መጡ።</b>\nአሁን ቦቱ በትክክል እየሰራ ነው። ምን ላግዝዎት?")
            elif user_text == "🛍 ዕቃዎችን እይ":
                send_message(chat_id, "በአሁኑ ሰዓት ዝርዝሩ ባዶ ነው።")
            elif user_text == "📞 እኛን ለማግኘት":
                send_message(chat_id, "በ @yitbarek6081 ያግኙን።")
            else:
                send_message(chat_id, f"መልእክትዎ ደርሶኛል፡ {user_text}")
        return "OK", 200
    return "<h1>Bot Server is Online!</h1>"
