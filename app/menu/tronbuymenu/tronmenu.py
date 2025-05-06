from kassa.kassa import create_tron_invoice
import telebot
from telebot import *
from telebot.callback_data import *
import database.db as db

def tronbuymenu(bot, message):
    file = open('Покупка валюты.jpg', 'rb')

    menubtn = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='Покупка BTC', callback_data='buy_BTC')
    btn2 = types.InlineKeyboardButton(text='Покупка ETH', callback_data='buy_ETH')
    btn3 = types.InlineKeyboardButton(text='Покупка LTC', callback_data='buy_LTC')
    btn4 = types.InlineKeyboardButton(text='Покупка SOL', callback_data='buy_SOL')
    btn5 = types.InlineKeyboardButton(text='Покупка TRX', callback_data='buy_TRX')
    btn6 = types.InlineKeyboardButton(text='Покупка USDT', callback_data='buy_USDT')
    btn7 = types.InlineKeyboardButton(text='Покупка XMR', callback_data='buy_XMR')
    menubtn.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_photo(message.chat.id, file, reply_markup=menubtn)