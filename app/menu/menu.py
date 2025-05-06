import telebot
from telebot import *
from telebot.callback_data import *

def glavnoe_menu(bot, message):
    """
    Отправляет главное меню бота пользователю.
    Перед отправкой меню, проверяет наличие файла главного меню и прикрепляет его к переменной Object Object
    Создается клавиатура формата прикрепления к сообщению
    с 4 callback data -> 
        1. buytron
        2. profile
        3. contact
        4. calculator
    
    Отправка сообщения с клавиатурой и фото главного меню
    
    Parameters:
        message (telegram.Message): Объект входящего сообщения.
    
    Returns:
        None
    """
    file = open('Главное меню.jpg', 'rb')
    menubtn = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='💵 Купить', callback_data='tronbuymemu')
    btn2 = types.InlineKeyboardButton(text='👤 Профиль', callback_data='profile')
    btn3 = types.InlineKeyboardButton(text='📗 Контакты', callback_data='contact')
    btn4 = types.InlineKeyboardButton(text='💱 Калькулятор', callback_data='calculator')
    btn5 = types.InlineKeyboardButton(text='🔁 Перевод пользователю', callback_data='transfer')
    menubtn.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_photo(message.chat.id, file, reply_markup=menubtn)