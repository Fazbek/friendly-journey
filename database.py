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
            'user_pr_count INTEGER, '
            'total REAL'
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


def get_pr():
    return sql.execute('SELECT pr_id, pr_name, pr_count FROM products;').fetchall()


def get_exact_pr(pr_id):
    return sql.execute('SELECT pr_name, pr_description, pr_count, pr_price, pr_photo '
                       'FROM products WHERE pr_id=?;', (pr_id,)).fetchone()


def add_pr_to_cart(user_id, user_pr, user_pr_count, total):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (user_id, user_pr, user_pr_count, total))
    connection.commit()


def add_pr(pr_name, pr_description, pr_count, pr_price, pr_photo):
    sql.execute('INSERT INTO products(pr_name, pr_description, pr_count, pr_price, pr_photo) '
                'VALUES(?, ?, ?, ?, ?);', (pr_name, pr_description, pr_count, pr_price, pr_photo))
    connection.commit()


def del_pr(pr_id):
    sql.execute('DELETE FROM products WHERE pr_id=?;', (pr_id,))
    connection.commit()


def change_pr_count(pr_id, new_count):
    current_count = sql.execute('SELECT pr_count FROM products WHERE pr_id=?;', (pr_id,)).fetchone()
    sql.execute('UPDATE products SET pr_count=? WHERE pr_id=?;',
                (current_count[0]+new_count, pr_id))
    connection.commit()


def check_pr():
    pr_check = sql.execute('SELECT * FROM products;')
    if pr_check.fetchone():
        return True
    else:
        return False


def show_cart(user_id):
    cart_check = sql.execute('SELECT * FROM cart WHERE id=?;', (user_id,))
    if cart_check.fetchone():
        return cart_check.fetchone()
    else:
        return False


def clear_cart(user_id):
    sql.execute('DELETE FROM cart WHERE id=?;', (user_id,))
    connection.commit()


def make_order(user_id):
    pr_name = sql.execute('SELECT user_pr_name FROM cart WHERE id=?;', (user_id,)).fetchone()
    user_pr_count = sql.execute('SELECT user_pr_count FROM cart WHERE id=?;',
                                (user_id,)).fetchone()
    current_count = sql.execute('SELECT pr_count FROM products WHERE pr_name=?;',
                                (pr_name[0],)).fetchone()
    sql.execute('UPDATE products SET pr_count=? WHERE pr_name=?;',
                (current_count[0]-user_pr_count[0], pr_name[0]))
    info = sql.execute('SELECT * FROM cart WHERE id=?;', (user_id,)).fetchone()
    address = sql.execute('SELECT location FROM users WHERE id=?;', (user_id,)).fetchone()
    sql.execute('DELETE FROM cart WHERE id=?;', (user_id,))
    connection.commit()
    return info, address
