import telebot
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    print("USER ID:", user_id)
    bot.send_message(message.chat.id, "Your ID has been logged. Check Render logs.")

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.send_message(message.chat.id, "Bot is working.")

print("Bot is running...")
bot.infinity_polling()
