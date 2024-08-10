import sqlite3

def new_user(user_id):
    try:
        try:
            c = sqlite3.connect('users.db')
            cursor = c.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users( user_id TEXT PRIMARY KEY, balance INTEGER, TRX_ADRESS TEXT, TRX_stat FLOAT )''')
            c.commit()
            cursor.close()
            c.close()
        except sqlite3.Error as error:
            print("Ошибка при создании/подключении к базе данных:", error)
            cursor.close()
            c.close()
        
        balance = 0
        TRX_ADRESS = 0
        TRX_stat = 0
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        if valid(user_id) == True:
            c.execute(
                "INSERT INTO users (user_id, balance, TRX_ADRESS, TRX_stat) VALUES (?,?,?,?)",
                (user_id, balance, TRX_ADRESS, TRX_stat)
            )
            conn.commit()
            c.close()
            return True
        else:
            c.close()
            return False

        '''
        Что будет в базе данных о пользователе?

        username- имя пользователя user_id
        TRX адрес
        balance - баланс пользователя RUB

        stat TRX - куплено TRX
        '''

    except Exception as e:
        print(e)

def get_profile(user_id):
    user = user_id
    print(user)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    print("0")
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user,))
    print("1")
    data = cursor.fetchone()
    print(data)
    conn.commit()
    cursor.close()
    conn.close()
    return data

def update_trx(user_id, trx):
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET TRX_ADRESS = ? WHERE user_id = ?", (trx, user_id))
        conn.commit()
        c.close()
        return True
    except Exception as e:
        print(e)
        return False

# проверяем есть ли у пользователя wallet    
def check_db(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT TRX_ADRESS FROM users WHERE user_id = ?", (user_id,))
    data = c.fetchone()
    conn.commit()
    c.close()
    conn.close()
    if data != "0":
        return data[0]
    else:
        return False

def update_balance(user_id, amount):
    """Обновляет баланс пользователя в базе данных.

    Args:
        user_id: ID пользователя.
        amount: Сумма, которую нужно добавить к балансу.
    """

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Получение текущего баланса
    c.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    current_balance = c.fetchone()

    if current_balance:
        current_balance = current_balance[0]  # Получение значения из кортежа

        # Обновление баланса
        new_balance = current_balance + amount
        c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))

        conn.commit()
        conn.close()
        return True  # Возвращаем True, если обновление прошло успешно
    else:
        conn.close()
        return False
    
def delete_user(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE user_id =?", (user_id,))
    conn.commit()
    c.close()
    conn.close()
    return True  # Возвращаем True, если удаление прошло успешно
    
def valid(user_id):
    return True