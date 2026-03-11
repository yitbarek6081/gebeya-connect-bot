import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties
import os

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
app = Flask(__name__)

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"ሰላም! የገበያ ኮኔክት ቦት በቨርሴል ላይ እየሰራ ነው። የላኩት መልእክት፡ {message.text}")

@app.route('/api/index', methods=['POST', 'GET'])
def handle_webhook():
    if request.method == 'POST':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        update = Update.model_validate(request.get_json(), context={"bot": bot})
        loop.run_until_complete(dp.feed_update(bot, update))
        return 'OK', 200
    return "<h1>የቦቱ ዳሽቦርድ</h1>"
