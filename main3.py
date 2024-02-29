import telebot
from telebot import types

# This is bot from video
token = "6711204286:AAFBsauhSX3Zkt_IqkKAe6RyzKxUrKo_PRI"
my_id = 6206970344

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button1 = types.KeyboardButton(text="Services")
    button2 = types.KeyboardButton(text="About us")
    button3 = types.KeyboardButton(text="Leave a request")
    keyboard.add(button1, button2, button3)
    bot.send_message(message.chat.id, "Welcome to company", reply_markup=keyboard)


@bot.message_handler(commands=["info"])
def test(message):
    keyboard = types.InlineKeyboardMarkup()
    url = types.InlineKeyboardButton(text="Link to our site", url="https://ya.ru")
    keyboard.add(url)
    bot.send_message(message.chat.id, "Information about our company", reply_markup=keyboard)


def send_request(message):
    mes = f"New bid: {message.text}"
    bot.send_message(my_id, mes)
    bot.send_message(message.chat.id, "Thank you for bid! Our specialists will connect with you")


def send_service(message):
    bot.send_message(message.chat.id, "1. Make yearly list")
    bot.send_message(message.chat.id, "2. Pay fees for TOO")
    bot.send_message(message.chat.id, "3. Count bujet")


@bot.message_handler(content_types=["text"])
def repeat_all(message):
    if message.text.lower() == "about us":
        test(message)
    elif message.text.lower() == "leave a request":
        bot.send_message(message.chat.id, "We'll be happy to serve you. Send us your number")
        bot.register_next_step_handler(message, send_request)
    elif message.text.lower() == "services":
        send_service(message)


bot.polling(non_stop=True)
