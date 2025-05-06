import telebot
from telebot import *
from telebot.callback_data import *
import database.db as db

def profile(bot, message):
    """
        Получаем id чата с пользователем для его идентификации
        Отправляем через file = open в память плашку профиль
        Запрашиваем данные из базы данных о пользователе

        Парсим данные внутрь переменных о
        1) Балансе
        2) Всего купленных TRX
        3) Установленном TRX-адресе

        Отрисовываем кнопки управления
        Отправляем сообщение пользователю с информацией о профиле
        Отправляем администратору сообщение о просмотре профиля
    """
    user_id = message.chat.id
    file = open('Мой профиль.jpg', 'rb')
    # Запрашиваем информацию из базу данных
    data = db.get_profile(user_id)
    # Парсим данные
    balance = data[1]
    balance_trx = data[3]
    trx_addr = data[2]

    usdt_addr = data[4]
    usdt_balance = data[5]

    btc_addr = data[6]
    btc_balance = data[7]

    ltc_addr = data[8]
    ltc_balance = data[9]

    sol_addr = data[10]
    sol_balance = data[11]

    xnr_addr = data[12]
    xnr_balance = data[13]

    eth_addr = data[14]
    eth_balance = data[15]
    # кнопки управления
    prof = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton(text='Пополнение баланса', callback_data='change_pay')
    but2 = types.InlineKeyboardButton(text='Адреса', callback_data='all_addr')
    prof.add(but1, but2)
    #Отправляем сообщение пользователю
    bot.send_photo(message.chat.id, file, f"""Информация о профиле клиента [ID: {user_id}]
Баланс: {balance} RUB
Всего куплено TRX: {balance_trx} TRX
Всего куплено USDT: {usdt_balance} USDT
Всего куплено BTC: {btc_balance} BTC
Всего куплено LTC: {ltc_balance} LTC
Всего куплено SOL(SOLANA): {sol_balance} SOL
Всего куплено XRP: {xnr_balance} XRP
Всего куплено ETH: {eth_balance} ETH""", reply_markup=prof)
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл профиль')