import asyncio
import json
from flask import Flask, request
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Update, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# የቦት ቶከን
TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"

app = Flask(__name__)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# የቁልፍ ሰሌዳ (Keyboard)
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 ዕቃዎችን እይ"), KeyboardButton(text="➕ ዕቃ መዝግብ")],
        [KeyboardButton(text="📞 እኛን ለማግኘት")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        f"<b>ሰላም {message.from_user.full_name}!</b>\nእንኳን ወደ ገበያ ኮኔክት በሰላም መጡ። ምን ላግዝዎት?",
        reply_markup=main_kb
    )

@dp.message(F.text == "🛍 ዕቃዎችን እይ")
async def list_items(message: types.Message):
    await message.answer("በአሁኑ ሰዓት በዝርዝር ውስጥ ምንም ዕቃ የለም።")

@dp.message(F.text == "📞 እኛን ለማግኘት")
async def contact_us(message: types.Message):
    await message.answer("ለማንኛውም ጥያቄ በ @yitbarek6081 ያግኙን።")

@app.route('/', methods=['POST', 'GET'])
@app.route('/api/index', methods=['POST', 'GET'])
async def webhook():
    if request.method == 'POST':
        update = Update.model_validate(await request.get_json(), context={"bot": bot})
        await dp.feed_update(bot, update)
        return "OK", 200
    return "<h1>Gebeya Connect Bot is Active!</h1>"

# ለ Vercel አስፈላጊ ነው
def handler(event, context):
    return app(event, context)
