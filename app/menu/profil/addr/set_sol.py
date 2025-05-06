import telebot
from telebot import *
from telebot.callback_data import *
import database.update_wallet as db_update_wallet

def set_sol(bot, message):
    """
    Вызывается при нажатии на кнопку "Установить TRX-адрес"
    Просим у пользователя ввести его SOL адрес,мы не отвечаем за корректность ввода
    Отправляем сообщением администратору
    Запускаем обработку ввода TRX-адреса
    """
    user_id = message.chat.id
    file = open('Установить адрес.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл функцию для сохранеия SOL кошелька')
    bot.send_photo(message.chat.id, file, f'Пожалуйста, введите адрес своего SOL-кошелька.')
    bot.register_next_step_handler(message, lambda msg: sol_user(bot, msg))


def sol_user(bot, message):
    """
        Получает сообщение пользователя
        Сохраняет TRX-адрес в базу данных по user_id
    """
    trx = message.text
    print(trx)
    user_id = message.chat.id
    # Сохраняем TRX-адрес в базу данных
    db_update_wallet.update_sol(user_id, trx)
    # Сообщаем пользователю что TRX-адрес сохранен
    bot.send_message(-4633769276, f'Пользователь {user_id} сохранил SOL кошелек, его адрес {trx}')
    bot.send_message(message.chat.id, f'Ваш SOL-кошелек сохранен')