"""
    Импортирует библиотеку sqlite3 для работа с базой данных sql lite 
    Примечание: При желании можно поменять и на обычный MySQL сервер, код будет 1 и тот же, достаточно поменяить то где написано sqlite3 в коде на корректные значения
"""
import sqlite3

def update_trx(user_id, trx):
    """
        Обновляет TRX адрес пользователя в базе данных.
    """
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
    
def update_sol(user_id, trx):
    """
        Обновляет TRX адрес пользователя в базе данных.
    """
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET SOL_ADRESS = ? WHERE user_id = ?", (trx, user_id))
        conn.commit()
        c.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def update_btc(user_id, trx):
    """
        Обновляет TRX адрес пользователя в базе данных.
    """
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET BTC_ADRESS = ? WHERE user_id = ?", (trx, user_id))
        conn.commit()
        c.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def update_eth(user_id, trx):
    """
        Обновляет TRX адрес пользователя в базе данных.
    """
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET ETH_ADRESS = ? WHERE user_id = ?", (trx, user_id))
        conn.commit()
        c.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def update_ltc(user_id, trx):
    """
        Обновляет TRX адрес пользователя в базе данных.
    """
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET LTC_ADRESS = ? WHERE user_id = ?", (trx, user_id))
        conn.commit()
        c.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def update_usdt(user_id, trx):
    """
        Обновляет TRX адрес пользователя в базе данных.
    """
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET USDT_ADRESS = ? WHERE user_id = ?", (trx, user_id))
        conn.commit()
        c.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def update_xrp(user_id, trx):
    """
        Обновляет TRX адрес пользователя в базе данных.
    """
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("UPDATE users SET XNR_ADRESS = ? WHERE user_id = ?", (trx, user_id))
        conn.commit()
        c.close()
        return True
    except Exception as e:
        print(e)
        return False