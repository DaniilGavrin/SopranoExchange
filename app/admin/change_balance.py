import database.db as db
import telebot
from telebot import *
from telebot.callback_data import *

"""
    Инициализация переменных
    balance_change_userid - идентификатор пользователя
    корректирующая переменная для изменения баланса пользователя
"""
balance_change_userid = ""

def change_balance(bot, message):
    """
        Административная функция для изменения баланса пользователя
        На этом шаге спрашиваем id пользователя цифровой
    """
    bot.send_message(-4633769276, "Запущена функция изменения баланса пользователя администратором.")
    bot.send_message(message.chat.id, "Напишите пожалуйста user_id пользователя которого необходимо изменить баланс или cancel для отмены")
    bot.register_next_step_handler(message, lambda msg: change_balance_user_id(bot,msg))

def change_balance_user_id(bot,message):
    """
        msg = сообщение об id пользователя
        Проверяем, если введенное значение равно cancel, то отменяем операцию
        Если введенное значение не cancel, то проверяем, является ли id числом
        Если id является числом, то переходим к следующему шагу
        Спрашиваем новый баланс пользователя
    """
    msg = message.text
    if msg == "cancel":
        bot.send_message(message.chat.id, "Удаление отменено.")
        bot.send_message(-4633769276, "Удаление отменено администратором")
    else:
        try:
            user_id = msg
            balance_change_userid = user_id
            print(balance_change_userid)
            bot.send_message(message.chat.id, "Введите новый баланс пользователя")
            bot.register_next_step_handler(message, lambda msg: change_balance_new_balance(bot,msg,user_id))
        except ValueError:
            bot.send_message(message.chat.id, "Введите корректное числовое значение user_id.")
            bot.send_message(-4633769276, "Возникла ошибка при изменении баланса пользователя")

def change_balance_new_balance(bot, message, user_id):
    """
        Переменной new_balance присваиваем значение сообщения перекидывая его в число
        Выводим как debug новый баланс и id пользователя.
        Обновляем баланс в базе данных и выводим сообщение об изменении.
    """
    try:
        new_balance = int(message.text)
        db.update_balance(user_id, new_balance)
        print(new_balance, user_id)
        bot.send_message(message.chat.id, f"Баланс пользователя с id {user_id} изменен на {new_balance}")
        bot.send_message(-4633769276, f"Баланс пользователя с id {user_id} изменен на {new_balance}")
    except ValueError:
        bot.send_message(message.chat.id, "Введите корректное числовое значение баланса.")
        bot.send_message(-4633769276, "Возникла ошибка при изменении баланса пользователя")