import telebot
from telebot import *
from telebot.callback_data import *
import database.db as db

def all_addr(bot, message):
    """
    Вызывается при нажатии на кнопку "Установить TRX-адрес"
    Отправляем сообщением администратору
    Запускаем обработку ввода TRX-адреса
    """
    user_id = message.chat.id
    data = db.get_profile(user_id)

    # Парсим данные
    trx_addr = data[2]
    usdt_addr = data[4]
    btc_addr = data[6]
    ltc_addr = data[8]
    sol_addr = data[10]
    xnr_addr = data[12]
    eth_addr = data[14]


    menubtn = types.InlineKeyboardMarkup(row_width=2)
    btn_trx = types.InlineKeyboardButton("TRON (TRX)", callback_data="set_trx")
    btn_usdt = types.InlineKeyboardButton("USDT (USDT)", callback_data="set_usdt")
    btn_btc = types.InlineKeyboardButton("BTC (BTC)", callback_data="set_btc")
    btn_ltc = types.InlineKeyboardButton("LTC (LTC)", callback_data="set_ltc")
    btn_sol = types.InlineKeyboardButton("SOLANA (SOL)", callback_data="set_sol")
    btn_xrp = types.InlineKeyboardButton("XRP (XRP)", callback_data="set_xrp")
    btn_eth = types.InlineKeyboardButton("ETH (ETH)", callback_data="set_eth")

    menubtn.add(
        btn_trx, 
        btn_usdt, 
        btn_btc, 
        btn_ltc, 
        btn_sol, 
        btn_xrp, 
        btn_eth
    )
    
    file = open('Установить адрес.jpg', 'rb')
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл функцию сохранённые адреса кошельков')
    bot.send_photo(message.chat.id, file, f"""Пожалуйста, выберите необходимую сеть для смены адреса
                   
Ваши адреса:
Установленный TRON (TRX) адрес: {trx_addr}
Установленный USDT (USDT) адрес: {usdt_addr}
Установленный BTC (BTC) адрес: {btc_addr}
Установленный LTC (LTC) адрес: {ltc_addr}
Установленный SOLANA (SOL) адрес: {sol_addr}
Установленный XRP (XRP) адрес: {xnr_addr}
Установленный ETH (ETH) адрес: {eth_addr}""", reply_markup=menubtn)