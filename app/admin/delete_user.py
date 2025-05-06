import database.db as db
import telebot
from telebot import *
from telebot.callback_data import *

def delete_user(bot, message):
    """
        Функция удаления пользователя
        Отдает сообщение администратора главному и спрашивает id пользователя
    """
    bot.send_message(-4633769276, "Запущена функция удаления пользователя администратором.")
    bot.send_message(message.chat.id, "Напишите пожалуйста user_id пользователя которого необходимо удалить или cancel для отмены")
    bot.register_next_step_handler(message, lambda msg: delete_user_id(bot, msg))

def delete_user_id(bot, message):
    """
        Функция принимает id пользователя и удаляет его из базы
        Отдает сообщение об успешном удалении
    """
    msg = message.text
    if msg == "cancel":
        bot.send_message(message.chat.id, "Удаление отменено.")
        bot.send_message(-4633769276, "Удаление отменено администратором")
    else:
        try:
            user_id = message.chat.id
            db.delete_user(msg)
            bot.send_message(message.chat.id, f"Пользователь удален.")
            bot.send_message(-4633769276, f"Пользователь удален.")
        except ValueError:
            bot.send_message(message.chat.id, "Введите корректное числовое значение user_id.")
            bot.send_message(-4633769276, "Возникла ошибка при удалении пользователя")