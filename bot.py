import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import WebAppInfo

app = Flask(__name__)

# Fallback token trực tiếp để test (sau xóa đi)
TOKEN = '7996792257:AAFf4YdcWX8nyCDXFwQLRhF0wsq6ZgAkf_0'
bot = Bot(token=TOKEN)

@app.route('/')
def home():
    return '<h1>Tiến Lên Miền Nam Mini App đang chạy!</h1>'

@app.route('/setwebhook')
def set_webhook():
    try:
        url = f"https://{request.host}/webhook"
        bot.set_webhook(url=url)
        return f'Webhook set! URL: {url}'
    except Exception as e:
        return f'Error: {str(e)}'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        if update and update.message and update.message.text:
            text = update.message.text.lower()
            if 'start' in text:
                keyboard = [[InlineKeyboardButton("Chơi Tiến Lên Miền Nam",
                          web_app=WebAppInfo(url="https://tienlen-miniapp.netlify.app"))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=update.message.chat.id,
                                 text="Mở bàn chơi ngay nào!",
                                 reply_markup=reply_markup)
    except Exception as e:
        print(f'Webhook error: {str(e)}')  # Log để xem trên Render
    return 'OK', 200

if __name__ == '__main__':
    app.run()
