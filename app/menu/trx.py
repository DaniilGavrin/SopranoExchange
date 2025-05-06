import requests
from menu.profil import profil
import menu.trx as trx
import telebot
from telebot import *
from telebot.callback_data import *

def kurs(bot, message):
    """
    Выводит значение с актуальным курсом рубля к TRX через запрос к функции trx.rub_to_trx_rate()
    Спрашиваем у пользователя количество TRX сколько он хочет узнать цену в рублях
    Передаем данные в следующую фукнцию
    """
    user_id = message.chat.id
    file = open('Калькулятор.jpg', 'rb')
    bot.send_photo(message.chat.id, file, f"Текущий курс рубля к TRX состоавляет:\n1 TRX равен {trx.rub_to_trx_rate()} рубля")
    print(rub_to_trx_rate())
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл курс валюты')
    bot.send_message(message.chat.id, f"Введите число TRX чтобы узнать сколько это будет в рублях или cancel для отмены.")
    bot.register_next_step_handler(message, lambda msg: trx_to_rub(bot, msg))

def trx_to_rub(bot, message):
    """
        Получаем ответ пользователя и если ответ отмена операции идет возврат в профиль
        Если ответ не отмена, то проверяем, является ли введенное значение числом
        Если введенное значение число, то вычисляем цену в рублях и отправляем пользователю
    """
    msg = message.text
    if msg.lower() == 'cancel':
        bot.send_message(message.chat.id, 'Отмена операции')
        profil.profile(bot, message)
    else:
        try:
            trx_user = float(msg)
            rub = trx.rub_to_trx_rate()
            rub2 = rub * trx_user
            print(rub2)
            bot.send_message(message.chat.id, f"{trx_user} TRX стоит {rub2} рублей")
        except ValueError:
            bot.send_message(message.chat.id, "Ошибка! Вы ввели не число!")

def rub_to_trx_rate():
    """
    Получение актуального курса рубля в TRX через запрос к API coingecko
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "tron",
        "vs_currencies": "rub"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["tron"]["rub"]