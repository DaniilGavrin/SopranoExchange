import telebot
from telebot import *
from telebot.callback_data import *
from course import TRX
from database import db
import database.transfer_wallet as db_transfer_wallet

def transfer_trx(bot, message):
    bot.send_message(message.chat.id, "Перевод TRX\n Введите пожалуйста ID клиента:")
    bot.register_next_step_handler(message, lambda msg: trx_transfer(bot, msg))

def trx_transfer(bot, message):
    try:
        user_id = int(message.text)
        if user_id == message.chat.id:
            bot.send_message(message.chat.id, "Нельзя перевести самому себе TRX.")
            return
        bot.send_message(message.chat.id, "Введите сумму TRX которую хотите перевести. Не менее 2 TRX")
        bot.register_next_step_handler(message, lambda msg: trx_transfer_sum(bot, msg, user_id))
    except ValueError:
        bot.send_message(message.chat.id, "Введено некорректное значение. Пожалуйста, введите число.")

def trx_transfer_sum(bot, message, user_id):
    try:
        sender_id = message.chat.id
        amount = float(message.text)
        
        if amount <= 0:
            bot.send_message(sender_id, "Сумма перевода должна быть положительной.")
            return
        
        if amount < 2:
            bot.send_message(sender_id, "Сумма слишком низкая")
            return 
        
        # Получаем текущий курс BTC
        trx_rate = TRX.get_trx_rate()
        if not trx_rate:
            bot.send_message(sender_id, "Ошибка получения курса. Попробуйте позже.")
            return
        
        print(f"trx_rate: {trx_rate}")
        rate = trx_rate * amount
        print(f'Будет списано: {rate}')
        bot.send_message(sender_id, f'С вашего счета будет списано {rate} Рублей. Ожидаю ответа о гарантии перевода от базы данных')

        # Получаем баланс пользователя
        data = db.get_profile(sender_id)
        balance = data[1]
        print(f"balance: {balance}")
        
        if rate > balance:
            bot.send_message(sender_id, f'Отказ базы данных, проверка завершена неуспешно, так как ваш баланс {balance}.\nА сумма перевода эквивалентна {rate}')
        
        bot.send_message(sender_id, f'База данных подтвердила перевод, начинаю процесс перевода денег. Если вы ошиблись с получателем то отменить транзацию можно только через тех поддержку.')
        if db_transfer_wallet.transfer_rub(sender_id, user_id, rate):
            bot.send_message(sender_id, f'Деньги списаны с баланса, перевод выполнен успешно')
            bot.send_message(user_id, f'Ваш баланс был пополнен, пользователем {sender_id}, на сумму {rate}, что в данном случаи эквивалентно {amount} TRX.')
            bot.send_message(-4633769276, f' Был выполнен перевод между пользователем {sender_id}, на сумму {rate}, пользователю {user_id} что в данном случаи эквивалентно {amount} TRX. Всё успешно отправлено пользователю.')
    except ValueError:
        bot.send_message(message.chat.id, "Введено некорректное значение суммы. Пожалуйста, введите число.")