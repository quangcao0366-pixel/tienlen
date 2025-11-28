import os
import json
from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import Application

app = Flask(__name__)

# Token từ Environment Variable (an toàn)
TOKEN = os.environ.get('TELEGRAM_TOKEN', '7996792257:AAFf4YdcWX8nyCDXFwQLRhF0wsq6ZgAkf_0')
bot = Bot(token=TOKEN)

@app.route('/')
def home():
    return '<h1>Tiến Lên Miền Nam Mini App đang chạy!</h1><p>Bot đã sẵn sàng. Vào Telegram gõ /start là thấy nút chơi ngay!</p>'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    try:
        url = f"https://{request.host}/webhook"
        bot.set_webhook(url=url)
        return 'Webhook set!'
    except Exception as e:
        return f'Error setting webhook: {str(e)}'

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Lấy JSON từ Telegram
        json_str = request.get_data(as_text=True)
        update = Update.de_json(json.loads(json_str), bot)
        
        if update and update.message:
            if '/start' in update.message.text:
                keyboard = [[InlineKeyboardButton("🎰 Chơi Tiến Lên Miền Nam", web_app=WebAppInfo("https://tienlen-miniapp.netlify.app"))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=update.message.chat.id, text="Mở bàn chơi ngay nào!", reply_markup=reply_markup)
                return 'OK'
        
        return 'OK'
    except Exception as e:
        return f'Webhook error: {str(e)}'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
