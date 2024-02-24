import telebot
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot("6711204286:AAFBsauhSX3Zkt_IqkKAe6RyzKxUrKo_PRI")

# First exersice


@bot.message_handler(commands=["site", "website"])
def site(message):
    webbrowser.open("https://youtube.com")


@bot.message_handler(commands=["file"])
def main(message):
    bot.send_message(message.chat.id, "Hello")


@bot.message_handler(commands=["help"])
def main(message):
    bot.send_message(message.chat.id, "<b>Help</b> <em>information</em>", parse_mode="html")


@bot.message_handler(commands=["hello"])
def main(message):
    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} {message.from_user.last_name}")


@bot.message_handler()
def info(message):
    if message.text.lower() == "hello":
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} {message.from_user.last_name}")
    elif message.text.lower() == "id":
        bot.reply_to(message, f"ID: {message.from_user.id}")


# Second exersice

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = (types.KeyboardButton("Open this site"))
    markup.row(btn1)
    btn2 = (types.KeyboardButton("Delete photo"))
    btn3 = (types.KeyboardButton("Change text"))
    markup.row(btn2, btn3)
    file = open("./photo.jpg", "rb")
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    bot.send_message(message.chat.id, "Hello", reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == "Open this site":
        bot.send_message(message.chat.id, "Website is open")
    elif message.text == "Delete photo":
        bot.send_message(message.chat.id, "Photo was deleted")


@bot.message_handler(content_types=["photo"])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = (types.InlineKeyboardButton("Open this site", url="https://google.com"))
    markup.row(btn1)
    btn2 = (types.InlineKeyboardButton("Delete photo", callback_data="delete"))
    btn3 = (types.InlineKeyboardButton("Change text", callback_data="edit"))
    markup.row(btn2, btn3)
    bot.reply_to(message, "This photo is beautiful", reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "delete":
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == "edit":
        bot.edit_message_text("Edit text", callback.message.chat.id, callback.message.message_id)

# Third exersice


name = None


@bot.message_handler(commands=["data"])
def data(message):
    con = sqlite3.connect("main.db")
    cur = con.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50));")
    con.commit()
    cur.close()

    bot.send_message(message.chat.id, "Hello , i will do registration! Write down your name")
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, "Write down the password")
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()
    con = sqlite3.connect("main.db")
    cur = con.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    con.commit()
    cur.close()
    con.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("List of users", callback_data="users"))
    bot.send_message(message.chat.id, "User has done registration", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    con = sqlite3.connect("main.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    info = ""
    for i in users:
        info += f"Name: {i[1]},  password: {i[2]}\n"

    cur.close()
    con.close()

    bot.send_message(call.message.chat.id, info)


bot.polling(non_stop=True)


