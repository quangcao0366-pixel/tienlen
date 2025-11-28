import os
import asyncio
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application

app = Flask(__name__)

TOKEN = os.environ.get('TELEGRAM_TOKEN', '7996792257:AAFf4YdcWX8nyCDXFwQLRhF0wsq6ZgAkf_0')
application = Application.builder().token(TOKEN).build()

@app.route('/')
def home():
    return '<h1>Tiến Lên Miền Nam đang chạy!</h1>'

@app.route('/setwebhook')
def set_webhook():
    url = f"https://{request.host}/webhook"
    asyncio.run(application.bot.set_webhook(url=url))
    return 'Webhook set!'

@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), application.bot)
        if update and update.message and update.message.text and 'start' in update.message.text.lower():
            keyboard = [[InlineKeyboardButton("Chơi Tiến Lên Miền Nam", web_app=InlineKeyboardButton.WebAppInfo("https://tienlen-miniapp.netlify.app"))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await application.bot.send_message(chat_id=update.message.chat.id, text="Mở bàn chơi ngay nào!", reply_markup=reply_markup)
    except Exception as e:
        pass
    return 'OK', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
