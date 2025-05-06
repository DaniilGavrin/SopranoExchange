import telebot
from telebot import *
from telebot.callback_data import *
import database.update_wallet as db_update_wallet

def set_ltc(bot, message):
    """
    Вызывается при нажатии на кнопку "Установить ltc-адрес"
    Просим у пользователя ввести его LTC адрес,мы не отвечаем за корректность ввода
    Отправляем сообщением администратору
    Запускаем обработку ввода ltc-адреса
    """
    user_id = message.chat.id
    file = open('Установить адрес.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл функцию для сохранеия LTC кошелька')
    bot.send_photo(message.chat.id, file, f'Пожалуйста, введите адрес своего LTC-кошелька.')
    bot.register_next_step_handler(message, lambda msg: ltc_user(bot, msg))


def ltc_user(bot, message):
    """
        Получает сообщение пользователя
        Сохраняет ltc-адрес в базу данных по user_id
    """
    ltc = message.text
    print(ltc)
    user_id = message.chat.id
    # Сохраняем ltc-адрес в базу данных
    db_update_wallet.update_ltc(user_id, ltc)
    # Сообщаем пользователю что ltc-адрес сохранен
    bot.send_message(-4633769276, f'Пользователь {user_id} сохранил LTC кошелек, его адрес {ltc}')
    bot.send_message(message.chat.id, f'Ваш LTC-кошелек сохранен')