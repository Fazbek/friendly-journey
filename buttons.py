from telebot import types


def num_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    number = types.KeyboardButton('Отправить номер', request_contact=True)
    kb.add(number)
    return kb


def loc_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('Отправить локацию', request_location=True)
    kb.add(location)
    return kb
