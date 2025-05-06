import telebot
from telebot import *
from telebot.callback_data import *

def contact(bot, message):
    """
        Функция передает данныес о контактах поддержки
        Открываем файл через file = open
        Создаем клавиатуру формата прикрепления к сообщению
        Отправляем сообщение с клавиатурой
        Отправляем администратору сообщение о просмотре контактов
    """
    user_id = message.chat.id
    file = open('Контакты сервиса.jpg', 'rb')
    cont = types.InlineKeyboardMarkup()
    admins = types.InlineKeyboardButton('Поддержка', url='tg://user?id=1006486795')
    cont.add(admins)
    bot.send_photo(message.chat.id, file, reply_markup=cont)
    bot.send_message(-4633769276, f'Пользователь {user_id} открыл контакты')