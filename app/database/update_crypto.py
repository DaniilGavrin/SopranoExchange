import sqlite3

def update_btc_balance(user_id, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Обновляем баланс в колонке BTC_stat
    c.execute("UPDATE users SET BTC_stat = ? WHERE user_id = ?", (balance, user_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def update_eth_balance(user_id, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Обновляем баланс в колонке ETH_stat
    c.execute("UPDATE users SET ETH_stat = ? WHERE user_id = ?", (balance, user_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def update_ltc_balance(user_id, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Обновляем баланс в колонке ltc_stat
    c.execute("UPDATE users SET LTC_stat = ? WHERE user_id = ?", (balance, user_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def update_sol_balance(user_id, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Обновляем баланс в колонке SOL_stat
    c.execute("UPDATE users SET SOL_stat = ? WHERE user_id = ?", (balance, user_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def update_trx_balance(user_id, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Обновляем баланс в колонке TRX_stat
    c.execute("UPDATE users SET TRX_stat = ? WHERE user_id = ?", (balance, user_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def update_usdt_balance(user_id, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Обновляем баланс в колонке USDT_stat
    c.execute("UPDATE users SET USDT_stat = ? WHERE user_id = ?", (balance, user_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()

def update_xmr_balance(user_id, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Обновляем баланс в колонке XNR_stat
    c.execute("UPDATE users SET XNR_stat = ? WHERE user_id = ?", (balance, user_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()