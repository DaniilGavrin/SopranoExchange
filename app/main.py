import telebot
from telebot import *
from telebot.callback_data import *
from settings import *
from kassa import *
import time

import math

import db

import trx

from crypto_pay_api_sdk import cryptopay

Crypto = cryptopay.Crypto("244640:AAMLyi8yUKRl1EYRHPQ3SGZMIoR5tEbXL4R", testnet = False)

balance_change_userid = ""

bot = TeleBot(
    TOKEN, parse_mode="HTML"
    )
    
@bot.message_handler(commands=['get'])
def get(message):
    user_id = message.chat.id
    bot.send_message(message.chat.id, f'Ваш id {user_id}')
    bot.send_message(-4253626554, f'Была выполнена команда /get пользователем {user_id}')

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Принять условия пользования', callback_data='accept_user')
    markup.add(button)
    bot.send_message(-4253626554, f'Была выполнена команда /start пользователем {user_id}')
    bot.send_message(message.chat.id, 'Привет! Я бот для обмена рублей на TRX. Нажмите на кнопку ниже.', reply_markup=markup)

# TODO: Написать панель администратора
@bot.message_handler(commands=['admin'])
def admin(message):
    user_id = message.chat.id
    if str(user_id) == settings.ADMIN_USER:
        bot.send_message(message.chat.id, 'Привет, администратор!')
        bot.send_message(-4253626554, f'Внимание в панель администратора был выполнен заход с аккаунта \n{user_id}\n@{message.chat.username}')
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text='Удалить аккаунт', callback_data='delete_user')
        button1 = types.InlineKeyboardButton(text='Изменить баланс пользователя', callback_data='change_balance')
        button2 = types.InlineKeyboardButton(text='Передать должность администратора', callback_data='change_admin')
        markup.add(button, button1, button2)
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав')
        bot.send_message(-4253626554, f"Внимаение в панель администратора пытается зайти не администратор. Попытка была выполнена с аккаунта \n{user_id}\n@{message.chat.username}")


def set_trx(bot, message):
    user_id = message.chat.id
    file = open('Адрес.png', 'rb')
    bot.send_message(-4253626554, f'Пользователь {user_id} открыл функцию для сохранеия TRON кошелька')
    bot.send_message(message.chat.id, f'Пожалуйста, введите адрес своего TRON-кошелька.')
    bot.register_next_step_handler(message, trx_user)


def trx_user(message):
    trx = message.text
    print(trx)
    user_id = message.chat.id
    # Сохраняем TRX-адрес в базу данных
    db.update_trx(user_id, trx)
    # Сообщаем пользователю что TRX-адрес сохранен
    bot.send_message(-4253626554, f'Пользователь {user_id} сохранил TRON кошелек, его адрес {trx}')
    bot.send_message(message.chat.id, f'Ваш TRON-кошелек сохранен')


def profile(bot, message):
    user_id = message.chat.id
    file = open('Профиль.png', 'rb')
    # Запрашиваем информацию из базу данных
    data = db.get_profile(user_id)
    # Парсим данные
    balance = data[1]
    balance_trx = data[3]
    trx_addr = data[2]
    # кнопки управления
    prof = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton(text='Пополнение баланса', callback_data='change_pay')
    but2 = types.InlineKeyboardButton(text='Установить TRX-адрес', callback_data='set_trx')
    prof.add(but1, but2)
    #Отправляем сообщение пользователю
    bot.send_photo(message.chat.id, file, f"""Информация о профиле клиента [ID: {user_id}]
Баланс: {balance} RUB
Всего куплено TRX: {balance_trx} TRX

Установленный TRON (TRX) адрес: {trx_addr}""", reply_markup=prof)
    bot.send_message(-4253626554, f'Пользователь {user_id} открыл профиль')

def kurs(bot, message):
    user_id = message.chat.id
    file = open('Калькулятор.png', 'rb')
    bot.send_photo(message.chat.id, file, f"Текущий курс рубля к TRX состоавляет:\n1 TRX равен {trx.rub_to_trx_rate()} рубля")
    print(trx.rub_to_trx_rate())
    bot.send_message(-4253626554, f'Пользователь {user_id} открыл курс валюты')
    bot.send_message(message.chat.id, f"Введите число TRX чтобы узнать сколько это будет в рублях или cancel для отмены.")
    bot.register_next_step_handler(message, trx_to_rub)

def trx_to_rub(message):
    msg = message.text
    if msg.lower() == 'cancel':
        bot.send_message(message.chat.id, 'Отмена операции')
        profile(bot, message)
    else:
        try:
            trx_user = float(msg)
            rub = trx.rub_to_trx_rate()
            rub2 = rub * trx_user
            print(rub2)
            bot.send_message(message.chat.id, f"{trx_user} TRX стоит {rub2} рублей")
        except ValueError:
            bot.send_message(message.chat.id, "Ошибка! Вы ввели не число!")

def contact(bot, message):
    user_id = message.chat.id
    file = open('Контакты.png', 'rb')
    cont = types.InlineKeyboardMarkup()
    admins = types.InlineKeyboardButton('Поддержка', url='tg://user?id=1006486795')
    cont.add(admins)
    bot.send_photo(message.chat.id, file, reply_markup=cont)
    bot.send_message(-4253626554, f'Пользователь {user_id} открыл контакты')

def accept_user(bot, message):
    print("1")
    user_id = message.chat.id
    bot.send_message(-4253626554, f'Пользователь {user_id} принял пользовательское соглашение')
    # Удаляем последнее сообщение от пользователя
    try:
        user = db.new_user(user_id)
        menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
        menu1 = types.KeyboardButton(text="📁 Главная")
        menu.add(menu1)
        if user == True:
            bot.send_message(message.chat.id, f"""🔥 Добро пожаловать в CryptoBot!
                             
CryptoBot - Ваш лучший автоматический помощник для эффективного и комфортного перевода RUB в TRX!
                             
Перед началом работы в нашем боте, прочтите условия пользования ботом.""", reply_markup=menu)
        else:
            bot.send_message(message.chat.id, 'Вы уже зарегистрированы! Повторная регистарция не требуется')
            bot.send_message(message.chat.id, """🔥 Добро пожаловать в CryptoBot!

CryptoBot - Ваш лучший автоматический помощник для эффективного и комфортного перевода RUB в TRX!

Перед началом работы в нашем боте, прочтите условия пользования ботом.""", reply_markup=menu)

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Ошибка при сохранении пользователя! Обратитесь к администратору!')

    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)


def change_pay(bot, message):
    user_id = message.chat.id
    buy = types.InlineKeyboardMarkup()
    npm1 = types.InlineKeyboardButton(text="CrystalPay", callback_data="buy_balance")
    npm2 = types.InlineKeyboardButton(text="CryptoBot", callback_data="buy_balance2")
    buy.add(npm1, npm2)
    bot.send_message(-4253626554, f'Пользователь {user_id} выбирает способ оплаты')
    bot.send_message(message.chat.id, 'Выберите способ оплаты', reply_markup=buy)

def buy(bot, message):
    user_id = message.chat.id
    file = open('Пополнение.png', 'rb')
    bot.send_message(-4253626554, f'Пользователь {user_id} выбрал crystalpay')
    bot.send_photo(message.chat.id, file, "💴 Введите сумму пополнения от 20.00₽:")
    bot.register_next_step_handler(message, create_payment)

def buy2(bot, message):
    user_id = message.chat.id
    file = open('Пополнение.png', 'rb')
    bot.send_message(-4253626554, f'Пользователь {user_id} выбрал CryptoBot')
    bot.send_photo(message.chat.id, file, "💴 Введите сумму пополнения от 1 TRX:")
    bot.register_next_step_handler(message, create_payment_crb)

def create_payment_crb(message):
    amount = message.text
    user_id = message.chat.id
    invoice = Crypto.createInvoice("TRX", amount, params={"description": "Пополнение баланса для MatrixExchange",
                                                 "expires_in": 600
                                                 })
    # Создаем кнопку "Перейти к оплате"
    result = invoice.get('result')
    print(invoice)
    print(result.get('pay_url'))
    markup = types.InlineKeyboardMarkup()
    pay_button = types.InlineKeyboardButton(text="Перейти к оплате", url=result.get('pay_url'))
    markup.add(pay_button)
    id = result.get('invoice_id')
    print(id)
    # Отправляем сообщение пользователю
    bot.send_message(user_id, f"Оплата через CryptoBot. в случаи проблем с оплатой обратитесь к администратору назвав идентификатор оплаты {result.get('invoice_id')}. Время на оплату 10 минут после платеж будет отменен", reply_markup=markup)
    bot.send_message(-4253626554, f'Пользователь {user_id} выполняет оплату. Выполняю проверку оплаты каждые 2 минуты. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}. В данный момент ручная проверка!! Платеж не будет зачислен автоматически!!!')
    if call.get('ok') == True:
        call = Crypto.getInvoices(params={'invoice_ids': id})
        result = call.get('result')
        items = result.get('items')
        while items[0].get('status') == 'active':
            time.sleep(60)
            bot.send_message(-4253626554, f"Выполняется проверка оплаты пользователем. идентификатор оплаты {result.get('invoice_id')}. Статус оплаты {items[0].get('status')}")
            pay_time += 1
            if pay_time == 10:
                bot.send_message(user_id, "Время на оплату закончилось. Отменяем платеж.")
                bot.send_message(-4253626554, f"Оплата не прошла успешно. Время на оплату закончилось. Отменяем платеж.")
                pay_time = 0
                break
        call = Crypto.getInvoices(params={'invoice_ids': id})
        result = call.get('result')
        items = result.get('items')
        if items[0].get('status') == 'paid':
            bot.send_message(user_id, "Оплата успешна. Зачисляем деньги на баланс. Деньги зачислим по курсу платежной системы.")
            bot.send_message(-4253626554, f"Оплата прошла успешно. Зачисляем деньги на баланс. Идентификатор оплаты {result.get('invoice_id')}. Деньги зачислим по курсу платежной системы.")
            curs = Crypto.getExchangeRates(params={'source': "TRX", 'target': "RUB"})
            result = curs.get('result')
            # Находим курс TRX к RUB
            for item in result:
                if item['source'] == 'TRX' and item['target'] == 'RUB':
                    rate = item['rate']
                    cost = rate * amount
                    commission = cost * 0.05
                    cost_comission = cost - commission
                    bot.send_message(-4253626554, f"Оплата прошла успешно. Зачисляем деньги на баланс. Идентификатор оплаты {result.get('invoice_id')}. Имя пользователя @{message.chat.username}. Деньги зачислим по курсу платежной системы. Зачислим пользователю {cost_comission}")
                    status_db = db.update_balance(user_id, amount)
                    if status_db == True:
                        bot.send_message(user_id, f"Оплата прошла успешно. Зачислено {cost_comission} рублей на баланс. Комиссия {commission} рублей. Баланс обновлен")
                        bot.send_message(-4253626554, f"Оплата прошла успешно. Зачислено {cost_comission} рублей на баланс. Комиссия {commission} рублей. Баланс обновлен. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}.")
                    else:
                        bot.send_message(-4253626554, f"Оплата прошла успешно, но в базе данных не удалось изменить баланс пользователя. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}. id пользователя {user_id}. Проверка выполняла в автоматическом режиме, и была успешной, проверьте базу данных!")
                    break
            else:
                rate = None  # Курс не найден
                bot.send_message(-4253626554, "Оплата была успешной, но в полатежкой системе не найден данный курс, проверьте логи и обратитесь к CryptoBot")

            if rate is not None:
                print(f"Курс TRX к RUB: {rate}")
            else:
                print("Курс TRX к RUB не найден")
        else:
            bot.send_message(user_id, "Оплата не была успешной, в платежкой системе ошибка. Обратитесь к администратору.")
            bot.send_message(-4253626554, f'Пользователь {user_id} выполнял оплату. Оплата не была успешной. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}. Проверка выполняла в автоматическом режиме, и не была успешной, проверьте JSON ответ по данному платежу!')

    else:
        bot.send_message(user_id, "Оплата не была успешной, в платежкой системе ошибка. Обратитесь к администратору.")
        bot.send_message(-4253626554, f'Пользователь {user_id} выполнял оплату. Оплата не была успешной, в платежкой системе ошибка. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}. Проверка выполняла в автоматическом режиме, и не была успешной, проверьте JSON ответ по данному платежу!')

def create_payment(message):
    pay_time = 0
    user_id = message.chat.id
    amount = message.text
    print(amount)
    invoice = create_invoice(amount)

    # Формируем сообщение для пользователя
    payment_info = f"""
💲 Платежная система: CrystalPay
К оплате: {amount}
ID-платежа: {invoice.get('id')}

Платеж проверяется автоматически каждую минуту. Время на оплату 10 минут.
"""
    
    # Создаем кнопку "Перейти к оплате"
    markup = types.InlineKeyboardMarkup()
    pay_button = types.InlineKeyboardButton(text="Перейти к оплате", url=invoice.get('url'))
    markup.add(pay_button)
    
    # Отправляем сообщение пользователю
    bot.send_message(user_id, payment_info, reply_markup=markup)
    bot.send_message(-4253626554, f'Пользователь {user_id} выполняет оплату информация об оплате\n{payment_info}')

    # Запускаем проверку платежа
    status = check_invoice_status(invoice.get('id'))
    print("huy")
    print(status.get('state'))
    while status.get('state') == 'notpayed':
        time.sleep(60)
        pay_time += 1
        if pay_time == 10:
            bot.send_message(-4253626554, f"Оплата не прошла успешно. Время на оплату закончилось. Отменяем платеж.")
            bot.send_message(user_id, "Время на оплату закончилось. Отменяем платеж.")
            pay_time = 0
            break
        status = check_invoice_status(invoice.get('id'))

    if status.get('state') == 'paid':
        data = db.get_profile(user_id)
        # Парсим данные
        balance = data[1]
        new_balance = status.get('amount')
        amount = new_balance - (new_balance / 100 * 5)
        bot.send_message(user_id, f"Оплата прошла успешно! Ваш баланс пополнен на {amount}")
        bot.send_message(-4253626554, f"Оплата прошла успешно. Зачисляем деньги на баланс. Имя пользователя @{message.chat.username}. Деньги зачислим по курсу платежной системы.")
        db.update_balance(user_id, amount)
        data = db.get_profile(user_id)
        # Парсим данные
        balance = data[1]
        bot.send_message(user_id, f"Ваш баланс: {balance}")
    else:
        bot.send_message(user_id, f"Оплата не удалась. Пожалуйста, попробуйте снова. Или обратитесь к администратору назвав идентификатор {status.get('id')}")
        bot.send_message(-4253626554, f"Оплата не удалась. Идентификатор пользователя {message.chat.id} Имя пользователя @{message.chat.username}. Отменяем платеж.")

def buy_tron(bot, message):
    file = open('Покупка.png', 'rb')
    bot.send_photo(message.chat.id, file, "Введите сумму покупки от 20 рублей:")
    bot.send_message(-4253626554, f"Идентификатор пользователя {message.chat.id} Имя пользователя @{message.chat.username}. Покупка TRON.")
    bot.register_next_step_handler(message, create_tron_payment)

def create_tron_payment(message):
    user_id = message.chat.id
    try:
        amount = int(message.text)
        amount = amount - (amount / 100 * 3)  # Считаем комиссию
        print(amount)
        wallet = db.check_db(user_id)

        # Проверяем достаточно ли денег на балансе пользователя
        data = db.get_profile(user_id)
        balance = data[1]

        if balance >= amount:
            if wallet != 0:
                invoice = create_tron_invoice(int(amount), wallet)
                if invoice != "3":
                    print(invoice)
                    # Формируем сообщение для пользователя
                    bot.send_message(message.chat.id, f" Ваш id вывода: {invoice.get('id')}\nОжидайте когда деньги поступят на кошелек")
                    bot.send_message(-4253626554, f"С пользователем {message.chat.id} не возникли проблемы.")
                else:
                    bot.send_message(user_id, 'Не удалось создать счет. Возникла проблема с кассой обратитесь к администратору')
                    bot.send_message(-4253626554, f"С пользователем {message.chat.id} возникли проблемы. Не удалось создать счет. На кассе нет средств для выполнения операции")
            else:
                bot.send_message(-4253626554, f"С пользователем {message.chat.id} возникли проблемы. Нет кошелька. Решаю вопрос автоматически")
                bot.send_message(user_id, 'У вас нет кошелька. Пожалуйста, введите существующий кошелек.')
                bot.register_next_step_handler(message, wallet_add)
        else:
            bot.send_message(user_id, 'Недостаточно средств на балансе.')

    except ValueError:
        bot.send_message(user_id, 'Введите корректное числовое значение.')
        bot.send_message(-4253626554, f"С пользователем {message.chat.id} возникли проблемы. Не хватает баланса.")
        # Возвращаем в главное меню
        glavnoe_menu(message)

def wallet_add(message):
    user_id = message.chat.id
    wallet = message.text
    db.update_wallet(user_id, wallet)
    bot.send_message(message.chat.id, "Ваш кошелек сохранен. Введите повторно сумму покупки от 20 рублей:")
    bot.send_message(-4253626554, f"Идентификатор пользователя {message.chat.id} Имя пользователя @{message.chat.username}. Кошелек сохранен в базу данных.")
    bot.register_next_step_handler(message, create_tron_payment)

def delete_user(bot, message):
    bot.send_message(-4253626554, "Запущена функция удаления пользователя администратором.")
    bot.send_message(message.chat.id, "Напишите пожалуйста user_id пользователя которого необходимо удалить или cancel для отмены")
    bot.register_next_step_handler(message, delete_user_id)

def delete_user_id(message):
    msg = message.text
    if msg == "cancel":
        bot.send_message(message.chat.id, "Удаление отменено.")
        bot.send_message(-4253626554, "Удаление отменено администратором")
    else:
        try:
            user_id = message.chat.id
            db.delete_user(msg)
            bot.send_message(message.chat.id, f"Пользователь удален.")
            bot.send_message(-4253626554, f"Пользователь удален.")
        except ValueError:
            bot.send_message(message.chat.id, "Введите корректное числовое значение user_id.")
            bot.send_message(-4253626554, "Возникла ошибка при удалении пользователя")

def change_balance(bot, message):
    bot.send_message(-4253626554, "Запущена функция изменения баланса пользователя администратором.")
    bot.send_message(message.chat.id, "Напишите пожалуйста user_id пользователя которого необходимо изменить баланс или cancel для отмены")
    bot.register_next_step_handler(message, change_balance_user_id)

def change_balance_user_id(message):
    msg = message.text
    if msg == "cancel":
        bot.send_message(message.chat.id, "Удаление отменено.")
        bot.send_message(-4253626554, "Удаление отменено администратором")
    else:
        try:
            user_id = msg
            balance_change_userid = user_id
            print(balance_change_userid)
            bot.send_message(message.chat.id, "Введите новый баланс пользователя")
            bot.register_next_step_handler(message, change_balance_new_balance, user_id)
        except ValueError:
            bot.send_message(message.chat.id, "Введите корректное числовое значение user_id.")
            bot.send_message(-4253626554, "Возникла ошибка при изменении баланса пользователя")

def change_balance_new_balance(message, user_id):
    try:
        new_balance = int(message.text)
        db.update_balance(user_id, new_balance)
        print(new_balance, user_id)
        bot.send_message(message.chat.id, f"Баланс пользователя с id {user_id} изменен на {new_balance}")
        bot.send_message(-4253626554, f"Баланс пользователя с id {user_id} изменен на {new_balance}")
    except ValueError:
        bot.send_message(message.chat.id, "Введите корректное числовое значение баланса.")
        bot.send_message(-4253626554, "Возникла ошибка при изменении баланса пользователя")

def change_admin(bot, message):
    bot.send_message(-4253626554, "Запущена функция изменения администратора администратором.")
    bot.send_message(message.chat.id, "Введите пожалуйста новый id администратора или cancel для отмены")
    bot.register_next_step_handler(message, change_admin_new_id)

def change_admin_new_id(message):
    msg = message.text
    if msg == "cancel":
        bot.send_message(message.chat.id, "Изменение отменено.")
        bot.send_message(-4253626554, "Изменение отменено администратором")
    else:
        try:
            new_admin_id = msg
            settings.ADMIN_USER = new_admin_id
            bot.send_message(message.chat.id, f"Администратор изменен на id {new_admin_id}")
            bot.send_message(-4253626554, f"Администратор изменен на id {new_admin_id}")
        except ValueError:
            bot.send_message(message.chat.id, "Введите корректные данные")
            bot.send_message(-4253626554, "Возникла ошибка при изменении администратора")

@bot.message_handler(content_types=['text'])
def text(message):
    if (message.text == "📁 Главная"):
        glavnoe_menu(message)
    elif (message.text == "cancel"):
        glavnoe_menu(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        if call.data == 'accept_user':
            print('accept_user')
            accept_user(bot, call.message)
        elif call.data == 'calculator':
            kurs(bot, call.message)
        elif call.data == 'contact':
            contact(bot, call.message)
        elif call.data == 'profile':
            profile(bot, call.message)
        elif call.data == 'buytron':
            buy_tron(bot, call.message)
        elif call.data == 'set_trx':
            set_trx(bot, call.message)
        elif call.data == 'buy_balance':
            buy(bot, call.message)
        elif call.data == 'buy_balance2':
            buy2(bot, call.message)
        elif call.data == 'change_pay':
            change_pay(bot, call.message)
        elif call.data == 'delete_user':
            delete_user(bot, call.message)
        elif call.data == 'change_balance':
            change_balance(bot, call.message)
        elif call.data == 'change_admin':
            change_admin(bot, call.message)
        else:
            print('unknown')
            bot.answer_callback_query(call.id, text='Неизвестная команда')
    except Exception as e:
        print(repr(e))

def glavnoe_menu(message):
    file = open('menu1.png', 'rb')
    menubtn = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='💵 Купить TRON', callback_data='buytron')
    btn2 = types.InlineKeyboardButton(text='👤 Профиль', callback_data='profile')
    btn3 = types.InlineKeyboardButton(text='📗 Контакты', callback_data='contact')
    btn4 = types.InlineKeyboardButton(text='💱 Калькулятор', callback_data='calculator')
    menubtn.add(btn1, btn2, btn3, btn4)
    bot.send_photo(message.chat.id, file, reply_markup=menubtn)

if __name__ == '__main__':
    bot.polling(none_stop=True)