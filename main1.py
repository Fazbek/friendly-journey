import sqlite3
import telebot
import buttons as bt
import database as db
from geopy import Nominatim


bot = telebot.TeleBot('6711204286:AAFBsauhSX3Zkt_IqkKAe6RyzKxUrKo_PRI')
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    check = db.check_user(user_id)
    if check:
        bot.send_message(user_id, 'Добро пожаловать в наш магазин!',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(user_id, 'Здравствуйте! '
                                  'Давайте проведем регистрацию!\n'
                                  'Напишите свое имя',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    user_id = message.from_user.id
    user_name = message.text
    bot.send_message(user_id, 'Супер, а теперь отправьте номер!',
                     reply_markup=bt.num_button())
    bot.register_next_step_handler(message, get_number, user_name)


def get_number(message, user_name):
    user_id = message.from_user.id
    if message.contact:
        user_number = message.contact.phone_number
        bot.send_message(user_id, 'А теперь локацию!',
                         reply_markup=bt.loc_button())
        bot.register_next_step_handler(message, get_location,
                                       user_name, user_number)
    else:
        bot.send_message(user_id, 'Отправьте номер по кнопке!',
                         reply_markup=bt.num_button())
        bot.register_next_step_handler(message, get_number, user_name)


def get_location(message, user_name, user_number):
    user_id = message.from_user.id
    if message.location:
        user_location = geolocator.reverse(f'{message.location.latitude}, '
                                           f'{message.location.longitude}')
        db.register(user_id, user_name, user_number, str(user_location))
        bot.send_message(user_id, 'Регистрация прошла упешно!')
    else:
        bot.send_message(user_id, 'Отправьте локацию через кнопку!',
                         reply_markup=bt.loc_button())
        bot.register_next_step_handler(message, get_location,
                                       user_name, user_number, greeting, callback)


def greeting(message):
    bot.send_message(message.from_user.id, f"Привет, {get_name}. 'Регистрация прошла упешно!")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    connection = sqlite3.connect("main.db")
    sql = connection.cursor()

    sql.execute("SELECT * FROM users")
    users = sql.fetchall()

    info = ""
    for i in users:
        info += f"Name: {i[1]},  password: {i[2]}\n"

    sql.close()
    connection.close()

    bot.send_message(call.message.chat.id, info)


bot.polling()
