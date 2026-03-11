import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties

# Flask App መጀመሪያ ይፈጠራል
app = Flask(__name__)

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# ቀለል ያለ ምላሽ
@dp.message()
async def handle_all(message: types.Message):
    if message.text == "/start":
        await message.answer("<b>ሰላም! ቦቱ አሁን በትክክል ሰርቷል።</b>\nእንኳን ደስ አለህ!")
    else:
        await message.answer(f"የላክኸው መልእክት፡ {message.text}")

# Vercel የሚፈልገው ዋናው Route
@app.route('/', defaults={'path': ''}, methods=['POST', 'GET'])
@app.route('/<path:path>', methods=['POST', 'GET'])
def home(path):
    if request.method == 'POST':
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            data = request.get_json()
            update = Update.model_validate(data, context={"bot": bot})
            loop.run_until_complete(dp.feed_update(bot, update))
            return "OK", 200
        except Exception as e:
            print(f"Error: {e}")
            return str(e), 500
    return "<h1>Bot is Online!</h1>"

# ይህ ለ Vercel Python Runtime በጣም ወሳኝ ነው
# 'app' የሚለው ስም ከ Flask app ስም ጋር ተመሳሳይ መሆን አለበት
