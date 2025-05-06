import telebot
from telebot import *
from telebot.callback_data import *
import database.update_wallet as db_update_wallet

def set_btc(bot, message):
    """
    Вызывается при нажатии на кнопку "Установить btc-адрес"
    Просим у пользователя ввести его BTC адрес,мы не отвечаем за корректность ввода
    Отправляем сообщением администратору
    Запускаем обработку ввода btc-адреса
    """
    user_id = message.chat.id
    file = open('Установить адрес.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл функцию для сохранеия BTC кошелька')
    bot.send_photo(message.chat.id, file, f'Пожалуйста, введите адрес своего BTC-кошелька.')
    bot.register_next_step_handler(message, lambda msg: btc_user(bot, msg))


def btc_user(bot, message):
    """
        Получает сообщение пользователя
        Сохраняет btc-адрес в базу данных по user_id
    """
    btc = message.text
    print(btc)
    user_id = message.chat.id
    # Сохраняем btc-адрес в базу данных
    db_update_wallet.update_btc(user_id, btc)
    # Сообщаем пользователю что btc-адрес сохранен
    bot.send_message(-4633769276, f'Пользователь {user_id} сохранил BTC кошелек, его адрес {btc}')
    bot.send_message(message.chat.id, f'Ваш BTC-кошелек сохранен')