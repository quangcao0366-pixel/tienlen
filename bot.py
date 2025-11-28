from flask import Flask, request, jsonify
import telegram
import os

TOKEN = "7996792257:AAFf4YdcWX8nyCDXFwQLRhF0wsq6ZgAkf_0"
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Tiến Lên Miền Nam Mini App đang chạy!</h1>
    <p>Bot đã sẵn sàng. Vào Telegram gõ @BotCuaBan là thấy nút chơi ngay!</p>
    '''

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    url = f"https://{request.host}/webhook"
    bot.set_webhook(url=url)
    return "Webhook set!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    if update.message:
        text = update.message.text
        chat_id = update.message.chat.id
        if text and "start" in text.lower():
            keyboard = [[telegram.InlineKeyboardButton("🎰 Chơi Tiến Lên Miền Nam", web_app=telegram.WebAppInfo("https://tienlen-miniapp.netlify.app"))]]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
            bot.send_message(chat_id=chat_id, text="Mở bàn chơi ngay nào!", reply_markup=reply_markup)
    return 'ok'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
