import telebot
import requests
import json

bot = telebot.TeleBot("6711204286:AAFBsauhSX3Zkt_IqkKAe6RyzKxUrKo_PRI")
API = "d4f96bae06923441cd5b82f3e720f229"


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello, nice to meet you!Write down the name of city")


@bot.message_handler(content_types=["text"])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f"Now weather: {data["main"]["temp"]}")

        image = "photo.png" if temp > 5.0 else "photo.png"
        file = open("./" + image, "rb")
        bot.send_message(message.chat.id, file)
    else:
        bot.reply_to(message, "City had written incorrectly")


bot.polling(non_stop=True)
