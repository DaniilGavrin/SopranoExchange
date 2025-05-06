import telebot
from telebot import *
from telebot.callback_data import *
import database.update_wallet as db_update_wallet

def set_xrp(bot, message):
    """
    Вызывается при нажатии на кнопку "Установить xrp-адрес"
    Просим у пользователя ввести его XRP адрес,мы не отвечаем за корректность ввода
    Отправляем сообщением администратору
    Запускаем обработку ввода xrp-адреса
    """
    user_id = message.chat.id
    file = open('Установить адрес.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл функцию для сохранеия XRP кошелька')
    bot.send_photo(message.chat.id, file, f'Пожалуйста, введите адрес своего XRP-кошелька.')
    bot.register_next_step_handler(message, lambda msg: xrp_user(bot, msg))


def xrp_user(bot, message):
    """
        Получает сообщение пользователя
        Сохраняет xrp-адрес в базу данных по user_id
    """
    xrp = message.text
    print(xrp)
    user_id = message.chat.id
    # Сохраняем xrp-адрес в базу данных
    db_update_wallet.update_xrp(user_id, xrp)
    # Сообщаем пользователю что xrp-адрес сохранен
    bot.send_message(-4633769276, f'Пользователь {user_id} сохранил XRP кошелек, его адрес {xrp}')
    bot.send_message(message.chat.id, f'Ваш XRP-кошелек сохранен')