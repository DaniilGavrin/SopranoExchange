import telebot
from telebot import *
from telebot.callback_data import *
import database.db as db

def accept_user(bot, message):
    """
    Принимает нового пользователя и отправляет приветственное сообщение с правилами бота.

    user_id - числовой id пользователя, получается из входящего последнего сообщения пользователя, которые достает id из chat по message.chat.id
    Отправляет сообщение администратору о принятии пользователем соглашения.

    try блок:
        Обращается к базе данных через модуль db и функцию new_user
        Через menu переменную и types -> menu создается клавиатура которая будет в чате пользователя около клавиатуры всегда
        user == True:
            Если верно то:
                Происходит запись файла главного меню в память,
                Отправка приветственного сообщения с активацией клавиатуры
            Если не верно то:
                Происходит запись файла главного меню в память,
                Отправка сообщения о том что повторная регистрация не требуется система нашла профиль старый
                Отправка приветственного сообщения с активацией клавиатуры
    except Exception as e блок:
        Блок предназначенный в случаи когда система выдала какую-то ошибку которая не может выполнить главный блок кода полностью

        Вывод ошибки в консоль
        Отправка администратору сообщкения об критической ошибке системы
        Отправка пользователю сообщения о проблеме и просьбе обращения к администратору

    Parameters:
        bot (TelegramBot): Объект бота Telegram.
        message (Message): Объект сообщения Telegram.

    Returns:
        None
    """
    print("1")
    user_id = message.chat.id
    bot.send_message(-4633769276, f'Пользователь {user_id} принял пользовательское соглашение')
    # Удаляем последнее сообщение от пользователя
    try:
        user = db.new_user(user_id)
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu1 = types.KeyboardButton(text="📁 Главная")
        menu.add(menu1)
        if user == True:
            file = open('Soprano exchange (2).jpg', 'rb')
            bot.send_photo(message.chat.id, file, """🔥 Добро пожаловать в CryptoBot!

CryptoBot - Ваш лучший автоматический помощник для эффективного и комфортного перевода RUB в TRX!

Перед началом работы в нашем боте, прочтите условия пользования ботом.""", reply_markup=menu)
        else:
            file = open('Soprano exchange (2).jpg', 'rb')
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы! Повторная регистрация не требуется')
            bot.send_photo(message.chat.id, file, """🔥 Добро пожаловать в CryptoBot!

CryptoBot - Ваш лучший автоматический помощник для эффективного и комфортного перевода RUB в TRX!

Перед началом работы в нашем боте, прочтите условия пользования ботом.""", reply_markup=menu)

    except Exception as e:
        print(e)
        bot.send_message(-4633769276, f"Внимание!! Авторизация пользователей не работает, в системе критическая ошибка! \n{e}")
        bot.send_message(message.chat.id, 'Ошибка при сохранении пользователя! Обратитесь к администратору! ')

    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)