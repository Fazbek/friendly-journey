import sqlite3


connection = sqlite3.connect('shop.db', check_same_thread=False)
sql = connection.cursor()


sql.execute('CREATE TABLE IF NOT EXISTS users ('
            'id INTEGER, '
            'name TEXT, '
            'number TEXT, '
            'location TEXT'
            ');')
sql.execute('CREATE TABLE IF NOT EXISTS products ('
            'pr_id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'pr_name TEXT, '
            'pr_count INTEGER, '
            'pr_description TEXT, '
            'pr_price REAL, '
            'pr_photo TEXT'
            ');')
sql.execute('CREATE TABLE IF NOT EXISTS cart ('
            'id INTEGER, '
            'user_pr_name TEXT, '
            'user_pr_count INTEGER'
            ');')


def check_user(id):
    check = sql.execute('SELECT * FROM users WHERE id=?;', (id,))
    if check.fetchone():
        return True
    else:
        return False


def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, number, location))
    connection.commit()

