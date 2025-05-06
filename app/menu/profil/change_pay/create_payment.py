from kassa import *
import telebot
from telebot import *
from telebot.callback_data import *
import database.db as db
from kassa.kassa import check_invoice_status, create_invoice

def create_payment(bot,message):
    """
        Функция для оплаты через систему платежей crystalpay
        Получаем сумму и id чата пользователя
        Создаем счет на оплату
        Создаем inline-кнопку для перехода к оплате
        Проверяем статус оплаты в цикле
        Если статус оплаты неоплачен, повторяем проверку через 1 минуту
        Если статус оплаты оплачен, отправляем сообщение об успешной оплате
        Отправляем сообщение администратору об оплате
        Обновляем баланс на стороне базы данных
    """
    print("Хуй 222")
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
    bot.send_message(-4633769276, f'Пользователь {user_id} выполняет оплату информация об оплате\n{payment_info}')

    # Запускаем проверку платежа
    status = check_invoice_status(invoice.get('id'))
    print("huy")
    print(status.get('state'))
    while status.get('state') == 'notpayed':
        time.sleep(60)
        pay_time += 1
        print(pay_time)
        if pay_time == 10:
            bot.send_message(-4633769276, f"Оплата не прошла успешно. Время на оплату закончилось. Отменяем платеж.")
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
        bot.send_message(-4633769276, f"Оплата прошла успешно. Зачисляем деньги на баланс. Имя пользователя @{message.chat.username}. Деньги зачислим по курсу платежной системы.")
        db.update_balance(user_id, amount)
        data = db.get_profile(user_id)
        # Парсим данные
        balance = data[1]
        bot.send_message(user_id, f"Ваш баланс: {balance}")
    else:
        bot.send_message(user_id, f"Оплата не удалась. Пожалуйста, попробуйте снова. Или обратитесь к администратору назвав идентификатор {status.get('id')}")
        bot.send_message(-4633769276, f"Оплата не удалась. Идентификатор пользователя {message.chat.id} Имя пользователя @{message.chat.username}. Отменяем платеж.")