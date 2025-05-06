import telebot
from telebot import *
from telebot.callback_data import *
import database.db as db
from menu.profil.change_pay import create_payment
from menu.profil.change_pay.create_payment_crb import create_payment_crb

def buy(bot, message):
    """
        Активируется при выборе пополнения балансе через систему платежей crystalpay
        Выводит картинку
        Отправляет запрос на сумму пополнения
    """
    user_id = message.chat.id
    file = open('Пополнение.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} выбрал crystalpay')
    bot.send_photo(message.chat.id, file, "💴 Введите сумму пополнения от 20.00₽:")
    bot.register_next_step_handler(message, lambda msg: create_payment.create_payment(bot, msg))

def buy2(bot, message):
    """
        Активируется при выборе пополнения балансе через систему платежей СryptoBot
        Выводит картинку
        Отправляет запрос на сумму пополнения
    """
    user_id = message.chat.id
    file = open('Пополнение.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} выбрал CryptoBot')
    bot.send_photo(message.chat.id, file, "💴 Введите сумму пополнения от 1 TRX:")
    bot.register_next_step_handler(message, lambda msg: create_payment_crb(bot, msg))