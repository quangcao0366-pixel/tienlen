import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

app = Flask(__name__)

TOKEN = "7996792257:AAFf4YdcWX8nyCDXFwQLRhF0wsq6ZgAkf_0"
bot = Bot(token=TOKEN)

@app.route('/')
def home():
    return '<h1>Tiến Lên Miền Nam Mini App đang chạy!</h1>'

# Hỗ trợ cả /setwebhook và /setwebhook/
@app.route('/setwebhook', methods=['GET', 'POST'])
@app.route('/setwebhook/', methods=['GET', 'POST'])
def set_webhook():
    url = f"https://{request.host}/webhook"
    result = bot.set_webhook(url=url)
    if result:
        return f'Webhook set thành công!<br>URL: {url}'
    else:
        return 'Lỗi khi set webhook'

# Hỗ trợ cả /webhook và /webhook/ (chính là fix lỗi cuối cùng)
@app.route('/webhook', methods=['POST'])
@app.route('/webhook/', methods=['POST'])
def webhook():
    try:
        update = Update.de_json(request.get_json(force=True), bot)
        if update and update.message and 'start' in update.message.text.lower():
            keyboard = [[InlineKeyboardButton("Chơi Tiến Lên Miền Nam",
                                              web_app=WebAppInfo(url="https://tienlen-miniapp.netlify.app"))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            bot.send_message(
                chat_id=update.message.chat.id,
                text="Mở bàn chơi ngay nào!",
                reply_markup=reply_markup
            )
    except Exception as e:
        print(e)
    return 'OK', 200

if __name__ == '__main__':
    app.run()
