"""
    Импорты библиотек

    telebot - Главная библиотека
    telebot.callback_data - импорт callback классов
    types - модуль для клавиатуры

    accept_user - модуль для работы с авторизацией пользователя
    buytron - модуль для работы с покупкой tron
    contact - модуль для работы с контактами
    menu - модуль для работы с меню
    profil - модуль для работы с профилем
    trx - модуль для работы с курсом
    set_trx - модуль для профиля о смене trx адреса
    
    db - модуль для работы с базой данных
    db_conn - подключение к базе данных
    
    cryptopay - модуль для работы с Cryptopay API
    kassa - модуль для работы с кассой

    settings - настроройки для бота
"""
from telebot import *
from telebot.callback_data import *

from accept_user import accept_user
import database.db as db
from menu.tronbuymenu.buycrypto.buy_BTC import buy_BTC
from menu.tronbuymenu.buycrypto.buy_TRX import buy_TRX
from menu.tronbuymenu.buycrypto.buy_SOL import buy_SOL
from menu.tronbuymenu.buycrypto.buy_XMR import buy_XMR
from menu.tronbuymenu.buycrypto.buy_ETH import buy_ETH
from menu.tronbuymenu.buycrypto.buy_LTC import buy_LTC
from menu.tronbuymenu.buycrypto.buy_USDT import buy_USDT
from menu.tronbuymenu.tronmenu import tronbuymenu
from menu.profil import *
from menu.profil.all_addr import all_addr
from menu.profil.change_pay.change_pay import change_pay
from menu.trans_fer import transfer_btc, transfer_eth, transfer_ltc, transfer_sol, transfer_trx, transfer_usdt, transfer_xrp
from menu.transfer import transfer
from kassa import *

from menu.profil.change_pay import buy_balance
import menu.trx as trx
import menu.menu as menu
import menu.profil.profil as profil
from menu.profil.addr import set_sol, set_trx, set_btc, set_eth, set_ltc, set_usdt, set_xrp
import menu.contact as contact
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import admin.delete_user as delete_user
import admin.change_balance as change_balance
import admin.change_admin as change_admin
from settings import settings
from settings.settings import TOKEN, ADMIN_USER

"""
    Инициализация работы с telebot API
    Args:
    - Токен бота, импортируется из настроек (const)
    - parse_mode - указывает способ обработки сообщений, в данном случае "HTML" - для корректного отображения тегов HTML
"""
bot = TeleBot(
    TOKEN, parse_mode="HTML"
    )


CHANNELS = [-1002050877052] 

def check_subscriptions(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            print(f"✅ Проверка {channel}: {status}")
            if status in ["left", "kicked"]:
                return False
        except Exception as e:
            print(f"❌ Ошибка проверки {channel}: {e}")
            return False
    return True
    
@bot.message_handler(commands=['start'])
def start(message):
    """
    Эта функция обрабатывает команду '/start'. Она отправляет пользователю приветственное сообщение,
    предлагает ему принять условия обслуживания и регистрирует идентификатор пользователя.
    
    А после принятия условий пользования перекидывает на accept_user и отправляет сообщение администратору

    Parameters:
        message (telegram.Message): объект входящего сообщения.

    Returns:
        None
    """
    user_id = message.chat.id
    if check_subscriptions(user_id):  
        bot.send_message(user_id, "✅ Вы подписаны на все каналы! Доступ разрешён.")
        user_id = message.chat.id
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Принять условия пользования', callback_data='accept_user')
        markup.add(button)
        bot.send_message(-4633769276, f'Была выполнена команда /start пользователем {user_id}')
        bot.send_message(message.chat.id, 'Привет! Я бот для обмена рублей на TRX. Нажмите на кнопку ниже.', reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        for channel in CHANNELS:
            markup.add(InlineKeyboardButton("✅ Я подписался", callback_data="check_sub"))

        bot.send_message(user_id, "❌ Вы не подписаны на все каналы! Подпишитесь, чтобы продолжить.\n@SopranoCommunity", reply_markup=markup)


@bot.message_handler(commands=['get'])
def get(message):
    user_id = message.chat.id
    bot.send_message(message.chat.id, f'Ваш id {user_id}')
    bot.send_message(-4633769276, f'Была выполнена команда /get пользователем {user_id}')

@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.chat.username
    if str(user_id) == settings.ADMIN_USER:
        bot.send_message(message.chat.id, 'Привет, администратор!')
        bot.send_message(-4633769276, f'Внимание в панель администратора был выполнен заход с аккаунта \n{user_id}\n@{message.chat.username}')
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Удалить аккаунт', callback_data='delete_user')
        button1 = types.InlineKeyboardButton(text='Изменить баланс пользователя', callback_data='change_balance')
        button2 = types.InlineKeyboardButton(text='Передать должность администратора', callback_data='change_admin')
        markup.add(button, button1, button2)
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав')
        bot.send_message(-4633769276, f"Внимаение в панель администратора пытается зайти не администратор. Попытка была выполнена с аккаунта \n{user_id}\n@{message.chat.username}")

@bot.message_handler(content_types=['text'])
def text(message):
    if (message.text == "📁 Главная"):
        menu.glavnoe_menu(bot, message)
    elif (message.text == "cancel"):
        menu.glavnoe_menu(bot, message)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_subscription_callback(call):
    user_id = call.message.chat.id
    if check_subscriptions(user_id):
        bot.send_message(user_id, "✅ Подписка подтверждена! Доступ разрешён.")
    else:
        bot.send_message(user_id, "❌ Вы всё ещё не подписаны! Подпишитесь и попробуйте снова.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == 'accept_user':
            print('accept_user')
            accept_user.accept_user(bot, call.message)

        elif call.data == 'calculator':
            trx.kurs(bot, call.message)

        elif call.data == 'contact':
            contact.contact(bot, call.message)

        elif call.data == 'profile':
            profil.profile(bot, call.message)
        elif call.data == 'tronbuymemu':
            tronbuymenu(bot, call.message)

        elif call.data == 'all_addr':
            all_addr(bot, call.message)
        elif call.data =='set_trx':
            set_trx.set_trx(bot, call.message)
        elif call.data == 'set_usdt':
            set_usdt.set_usdt(bot, call.message)
        elif call.data == 'set_btc':
            set_btc.set_btc(bot, call.message)
        elif call.data == 'set_ltc':
            set_ltc.set_ltc(bot, call.message)
        elif call.data == 'set_sol':
            set_sol.set_sol(bot, call.message)
        elif call.data == 'set_xrp':
            set_xrp.set_xrp(bot, call.message)
        elif call.data == 'set_eth':
            set_eth.set_eth(bot, call.message)
        
        elif call.data == 'buy_BTC':
            buy_BTC(bot, call.message)
        elif call.data == 'buy_TRX':
            buy_TRX(bot, call.message)
        elif call.data == 'buy_SOL':
            buy_SOL(bot, call.message)
        elif call.data == 'buy_XMR':
            buy_XMR(bot, call.message)
        elif call.data == 'buy_ETH':
            buy_ETH(bot, call.message)
        elif call.data == 'buy_LTC':
            buy_LTC(bot, call.message)
        elif call.data == 'buy_USDT':
            buy_USDT(bot, call.message)

        elif call.data == 'buy_balance':
            buy_balance.buy(bot, call.message)
        elif call.data == 'buy_balance2':
            buy_balance.buy2(bot, call.message)

        elif call.data == 'change_pay':
            change_pay(bot, call.message)

        elif call.data == 'delete_user':
            delete_user.delete_user(bot, call.message)

        elif call.data == 'change_balance':
            change_balance.change_balance(bot, call.message)
            
        elif call.data == 'change_admin':
            change_admin.change_admin(bot, call.message)

        elif call.data == 'transfer':
            transfer(bot, call.message)
        elif call.data =='transfer_trx':
            transfer_trx.transfer_trx(bot, call.message)
        elif call.data == 'transfer_usdt':
            transfer_usdt.transfer_usdt(bot, call.message)
        elif call.data == 'transfer_btc':
            transfer_btc.transfer_btc(bot, call.message)
        elif call.data == 'transfer_ltc':
            transfer_ltc.transfer_ltc(bot, call.message)
        elif call.data == 'transfer_sol':
            transfer_sol.transfer_sol(bot, call.message)
        elif call.data == 'transfer_xrp':
            transfer_xrp.transfer_xrp(bot, call.message)
        elif call.data == 'transfer_eth':
            transfer_eth.transfer_eth(bot, call.message)
        else:
            print('unknown')
            bot.answer_callback_query(call.id, text='Неизвестная команда')
    except Exception as e:
        print(repr(e))

if __name__ == '__main__':
    bot.polling(none_stop=True)
    print("Бот запущен")