import telebot
from telebot import *
from telebot.callback_data import *
import database.db as db
from crypto_pay_api_sdk import cryptopay

Crypto = cryptopay.Crypto("244640:AAMLyi8yUKRl1EYRHPQ3SGZMIoR5tEbXL4R", testnet = False)

def create_payment_crb(bot, message):
    """
        Получаем сумму от пользователя
        Получаем id пользователя
        Создаем invoice на оплату
        Создаем кнопку "Перейти к оплате"
        Отправляем сообщение пользователю
        Отправляем сообщение администратору с идентификатором оплаты и пользователем
        В течении 10 минут проверяем прошла ли оплата
        В случаи оплаты зачисляем деньги на баланс в случаи не оплаты отменяем платеж и выводим сообщение
    """
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
    bot.send_message(-4633769276, f"Пользователь {user_id} выполняет оплату. Выполняю проверку оплаты каждые 2 минуты. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}. В данный момент ручная проверка!! Платеж не будет зачислен автоматически!!!")
    if call.get('ok') == True:
        call = Crypto.getInvoices(params={'invoice_ids': id})
        result = call.get('result')
        items = result.get('items')
        while items[0].get('status') == 'active':
            time.sleep(60)
            bot.send_message(-4633769276, f"Выполняется проверка оплаты пользователем. идентификатор оплаты {result.get('invoice_id')}. Статус оплаты {items[0].get('status')}")
            pay_time += 1
            if pay_time == 10:
                bot.send_message(user_id, "Время на оплату закончилось. Отменяем платеж.")
                bot.send_message(-4633769276, f"Оплата не прошла успешно. Время на оплату закончилось. Отменяем платеж.")
                pay_time = 0
                break
        call = Crypto.getInvoices(params={'invoice_ids': id})
        result = call.get('result')
        items = result.get('items')
        if items[0].get('status') == 'paid':
            bot.send_message(user_id, "Оплата успешна. Зачисляем деньги на баланс. Деньги зачислим по курсу платежной системы.")
            bot.send_message(-4633769276, f"Оплата прошла успешно. Зачисляем деньги на баланс. Идентификатор оплаты {result.get('invoice_id')}. Деньги зачислим по курсу платежной системы.")
            curs = Crypto.getExchangeRates(params={'source': "TRX", 'target': "RUB"})
            result = curs.get('result')
            # Находим курс TRX к RUB
            for item in result:
                if item['source'] == 'TRX' and item['target'] == 'RUB':
                    rate = item['rate']
                    cost = rate * amount
                    commission = cost * 0.05
                    cost_comission = cost - commission
                    bot.send_message(-4633769276, f"Оплата прошла успешно. Зачисляем деньги на баланс. Идентификатор оплаты {result.get('invoice_id')}. Имя пользователя @{message.chat.username}. Деньги зачислим по курсу платежной системы. Зачислим пользователю {cost_comission}")
                    status_db = db.update_balance(user_id, amount)
                    if status_db == True:
                        bot.send_message(user_id, f"Оплата прошла успешно. Зачислено {cost_comission} рублей на баланс. Комиссия {commission} рублей. Баланс обновлен")
                        bot.send_message(-4633769276, f"Оплата прошла успешно. Зачислено {cost_comission} рублей на баланс. Комиссия {commission} рублей. Баланс обновлен. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}.")
                    else:
                        bot.send_message(-4633769276, f"Оплата прошла успешно, но в базе данных не удалось изменить баланс пользователя. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}. id пользователя {user_id}. Проверка выполняла в автоматическом режиме, и была успешной, проверьте базу данных!")
                    break
            else:
                rate = None  # Курс не найден
                bot.send_message(-4633769276, "Оплата была успешной, но в полатежкой системе не найден данный курс, проверьте логи и обратитесь к CryptoBot")

            if rate is not None:
                print(f"Курс TRX к RUB: {rate}")
            else:
                print("Курс TRX к RUB не найден")
        else:
            bot.send_message(user_id, "Оплата не была успешной, в платежкой системе ошибка. Обратитесь к администратору.")
            bot.send_message(-4633769276, f"Пользователь {user_id} выполнял оплату. Оплата не была успешной. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}. Проверка выполняла в автоматическом режиме, и не была успешной, проверьте JSON ответ по данному платежу!")

    else:
        bot.send_message(user_id, "Оплата не была успешной, в платежкой системе ошибка. Обратитесь к администратору.")
        bot.send_message(-4633769276, f"Пользователь {user_id} выполнял оплату. Оплата не была успешной, в платежкой системе ошибка. Идентификатор оплаты {result.get('invoice_id')}. имя пользователя @{message.chat.username}. Проверка выполняла в автоматическом режиме, и не была успешной, проверьте JSON ответ по данному платежу!")
