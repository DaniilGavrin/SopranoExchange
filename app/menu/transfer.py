import telebot
from telebot import *
from telebot.callback_data import *


def transfer(bot, message):
    """
    Функция перевода между пользователями
    """
    user_id = message.chat.id

    menubtn = types.InlineKeyboardMarkup(row_width=2)
    btn_trx = types.InlineKeyboardButton("TRON (TRX)", callback_data="transfer_trx")
    btn_usdt = types.InlineKeyboardButton("USDT (USDT)", callback_data="transfer_usdt")
    btn_btc = types.InlineKeyboardButton("BTC (BTC)", callback_data="transfer_btc")
    btn_ltc = types.InlineKeyboardButton("LTC (LTC)", callback_data="transfer_ltc")
    btn_sol = types.InlineKeyboardButton("SOLANA (SOL)", callback_data="transfer_sol")
    btn_xrp = types.InlineKeyboardButton("XMR (XMR)", callback_data="transfer_xrp")
    btn_eth = types.InlineKeyboardButton("ETH (ETH)", callback_data="transfer_eth")

    menubtn.add(
        btn_trx, 
        btn_usdt, 
        btn_btc, 
        btn_ltc, 
        btn_sol, 
        btn_xrp, 
        btn_eth
    )

    

    bot.send_message(-4633769276, f'Пользователь {user_id} открыл меню перевода между пользователями')
    bot.send_message(message.chat.id, "Привет, ты попал в меню перевода между пользователями. Выбери валюту которую ты хочешь перевести другому пользователю.", reply_markup=menubtn)