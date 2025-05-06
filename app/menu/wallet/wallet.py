import menu.menu as menu
import telebot
from telebot import *
from telebot.callback_data import *
import menu.wallet.wallet as wallet
import database.db as db
from kassa import *

def wallet_add(bot, message):
    """
        Функция для ситуаций когда пользователь забыл создать кошелек и он его вводит и мы повторно спрашиваем сумму
        И уже эти данные передаем в create_tron_payment
    """
    user_id = message.chat.id
    wallet = message.text
    db.update_wallet(user_id, wallet)
    bot.send_message(message.chat.id, "Ваш кошелек сохранен. Введите повторно сумму покупки от 20 рублей:")
    bot.send_message(-4633769276, f"Идентификатор пользователя {message.chat.id} Имя пользователя @{message.chat.username}. Кошелек сохранен в базу данных.")