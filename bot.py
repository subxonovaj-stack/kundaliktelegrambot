import os
from flask import Flask, request
import telebot
from automation import run_automation

BOT_TOKEN = os.environ.get("BOT_TOKEN")
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")

# 🔒 PUT YOUR MOM'S TELEGRAM USER ID HERE
ALLOWED_USER_ID = 123456789  # <-- CHANGE THIS

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ---------------------------
# TELEGRAM HANDLER
# ---------------------------
@bot.message_handler(commands=['start'])
def handle_start(message):

    # 🔒 Restrict access
    if message.from_user.id != ALLOWED_USER_ID:
        bot.send_message(message.chat.id, "Access denied.")
        return

    bot.send_message(message.chat.id, "Process started...")

    # List of parents (PUT REAL ACCOUNTS HERE)
    parents = [
        {"username": "parent1_login", "password": "parent1_password"},
        {"username": "parent2_login", "password": "parent2_password"},
    ]

    # This function will send messages to Telegram
    def notify(text):
        bot.send_message(message.chat.id, text)

    # Run automation
    run_automation(parents, notify)

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
