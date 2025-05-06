"""
    Импортирует библиотеку sqlite3 для работа с базой данных sql lite 
    Примечание: При желании можно поменять и на обычный MySQL сервер, код будет 1 и тот же, достаточно поменяить то где написано sqlite3 в коде на корректные значения
"""
import sqlite3

def transfer_rub(sender_id, receiver_id, amount):
    """
    Переводит BTC с одного счета на другой.
    """
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    
    # Вычитаем сумму у отправителя
    c.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (amount, sender_id))
    
    # Добавляем сумму получателю
    c.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (amount, receiver_id))
    
    conn.commit()
    conn.close()
    return True