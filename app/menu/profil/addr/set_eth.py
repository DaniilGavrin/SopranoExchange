import telebot
from telebot import *
from telebot.callback_data import *
import database.update_wallet as db_update_wallet

def set_eth(bot, message):
    """
    Вызывается при нажатии на кнопку "Установить eth-адрес"
    Просим у пользователя ввести его ETH адрес,мы не отвечаем за корректность ввода
    Отправляем сообщением администратору
    Запускаем обработку ввода eth-адреса
    """
    user_id = message.chat.id
    file = open('Установить адрес.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл функцию для сохранеия ETH кошелька')
    bot.send_photo(message.chat.id, file, f'Пожалуйста, введите адрес своего ETH-кошелька.')
    bot.register_next_step_handler(message, lambda msg: eth_user(bot, msg))


def eth_user(bot, message):
    """
        Получает сообщение пользователя
        Сохраняет eth-адрес в базу данных по user_id
    """
    eth = message.text
    print(eth)
    user_id = message.chat.id
    # Сохраняем eth-адрес в базу данных
    db_update_wallet.update_eth(user_id, eth)
    # Сообщаем пользователю что eth-адрес сохранен
    bot.send_message(-4633769276, f'Пользователь {user_id} сохранил ETH кошелек, его адрес {eth}')
    bot.send_message(message.chat.id, f'Ваш ETH-кошелек сохранен')