import os
import telebot
from login_bot import run_login_cycle

BOT_TOKEN = os.environ.get("BOT_TOKEN")

print("BOT TOKEN EXISTS:", bool(BOT_TOKEN))

bot = telebot.TeleBot(BOT_TOKEN)

# Prevent double execution
is_running = False


@bot.message_handler(commands=['start'])
def handle_start(message):
    global is_running

    if is_running:
        bot.send_message(message.chat.id, "Process already running.")
        return

    is_running = True
    bot.send_message(message.chat.id, "Process started...")

    try:
        run_login_cycle(bot, message.chat.id)
        bot.send_message(message.chat.id, "All accounts finished.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {e}")

    is_running = False


print("Bot is running in polling mode...")
bot.infinity_polling()
