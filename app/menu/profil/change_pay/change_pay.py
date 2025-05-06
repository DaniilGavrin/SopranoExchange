import telebot
from telebot import *
from telebot.callback_data import *
import database.db as db

def change_pay(bot, message):
    """
        Получаем id чата с пользователем для его идентификации
        Отправляем через file = open в память изображение
        Отправляет сообщение администратору
    """
    user_id = message.chat.id
    buy = types.InlineKeyboardMarkup()
    npm1 = types.InlineKeyboardButton(text="CrystalPay", callback_data="buy_balance")
    npm2 = types.InlineKeyboardButton(text="CryptoBot", callback_data="buy_balance2")
    buy.add(npm1, npm2)
    bot.send_message(-4633769276, f'Пользователь {user_id} выбирает способ оплаты')
    bot.send_message(message.chat.id, 'Выберите способ оплаты', reply_markup=buy)