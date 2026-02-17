import os
from flask import Flask, request
import telebot
from login_bot import run_login_cycle

BOT_TOKEN = os.environ.get("8412268679:AAGLuk1jhw5R_6I3XZbdk-vAB17NTTfOHts")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")
print("BOT TOKEN EXISTS:", bool(BOT_TOKEN))


bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ---------------------------
# TELEGRAM HANDLER
# ---------------------------
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Process started...")
    run_login_cycle(bot, message.chat.id)
    bot.send_message(message.chat.id, "All accounts finished.")

# ---------------------------
# WEBHOOK ROUTE
# ---------------------------
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot is running."

# ---------------------------
# START SERVER
# ---------------------------
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
