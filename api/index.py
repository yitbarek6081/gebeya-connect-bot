import asyncio
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties

TOKEN = "7863843221:AAF5p6Rr6yJ-wDwUjD4YdbnhKUnnGjC8vmE"
app = Flask(__name__)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

# Buttons ዝግጅት
kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 ዕቃዎችን እይ"), KeyboardButton(text="➕ ዕቃ መዝግብ")],
        [KeyboardButton(text="📞 እኛን ለማግኘት")]
    ],
    resize_keyboard=True
)

@dp.message()
async def handle_message(message: types.Message):
    if message.text == "/start":
        await message.answer(f"<b>ሰላም {message.from_user.first_name}!</b>\nእንኳን ወደ ገበያ ኮኔክት በሰላም መጡ።", reply_markup=kb)
    elif message.text == "🛍 ዕቃዎችን እይ":
        await message.answer("አሁን ላይ ምንም የተመዘገበ ዕቃ የለም።")
    else:
        await message.answer("መልእክትዎ ደርሶኛል!")

@app.route('/', methods=['POST', 'GET'])
@app.route('/api/index', methods=['POST', 'GET'])
def webhook():
    if request.method == 'POST':
        # ይህ ክፍል ቴሌግራም የሚልከውን መረጃ ያስተናግዳል
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = request.get_json()
        update = Update.model_validate(data, context={"bot": bot})
        loop.run_until_complete(dp.feed_update(bot, update))
        return "OK", 200
    return "<h1>Gebeya Connect Server is Online!</h1>"
