import telebot
from login_bot import run_cycle

TOKEN = "8412268679:AAE5-pVOIM5rsTFmgOWVxYt61Q3UzB_gZlI"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def handle_start(message):

    bot.reply_to(message, "Process started...")

    def send_update(text):
        bot.send_message(message.chat.id, text)

    result = run_cycle(send_update)

    if result == "captcha":
        bot.send_message(message.chat.id, "Captcha appeared. Try again after an hour.")
    else:
        bot.send_message(message.chat.id, "All accounts finished.")


print("Bot is running...")
bot.infinity_polling()
