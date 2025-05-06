"""
    Импортирует библиотеку sqlite3 для работа с базой данных sql lite 
    Примечание: При желании можно поменять и на обычный MySQL сервер, код будет 1 и тот же, достаточно поменяить то где написано sqlite3 в коде на корректные значения
"""
import sqlite3

def update_balance(user_id, balance):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    # Обновляем баланс в колонке balance
    c.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance, user_id))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
