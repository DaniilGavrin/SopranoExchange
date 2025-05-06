import telebot
from telebot import *
from telebot.callback_data import *
import database.update_wallet as db_update_wallet

def set_usdt(bot, message):
    """
    Вызывается при нажатии на кнопку "Установить usdt-адрес"
    Просим у пользователя ввести его USDT адрес,мы не отвечаем за корректность ввода
    Отправляем сообщением администратору
    Запускаем обработку ввода usdt-адреса
    """
    user_id = message.chat.id
    file = open('Установить адрес.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл функцию для сохранеия USDT кошелька')
    bot.send_photo(message.chat.id, file, f'Пожалуйста, введите адрес своего USDT-кошелька.')
    bot.register_next_step_handler(message, lambda msg: usdt_user(bot, msg))


def usdt_user(bot, message):
    """
        Получает сообщение пользователя
        Сохраняет usdt-адрес в базу данных по user_id
    """
    usdt = message.text
    print(usdt)
    user_id = message.chat.id
    # Сохраняем usdt-адрес в базу данных
    db_update_wallet.update_usdt(user_id, usdt)
    # Сообщаем пользователю что usdt-адрес сохранен
    bot.send_message(-4633769276, f'Пользователь {user_id} сохранил USDT кошелек, его адрес {usdt}')
    bot.send_message(message.chat.id, f'Ваш USDT-кошелек сохранен')