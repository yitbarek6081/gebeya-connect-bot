from flask import Flask, request
import urllib.request
import json

app = Flask(__name__)

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"

@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def handler(path):
    if request.method == 'POST':
        data = request.get_json()
        if data and "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_text = data["message"].get("text", "")
            
            # መልእክት ለመላክ
            url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
            payload = json.dumps({
                "chat_id": chat_id, 
                "text": f"እንኳን ደስ አለህ! ቦቱ አሁን ሰርቷል። የላከው መልእክት፡ {user_text}"
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
            
        return "OK", 200
    
    return "<h1>Bot is Active!</h1>", 200
