from database import update_balance, update_crypto
from kassa.kassa import create_ltc_invoice
from course.LTC import get_ltc_rate
import menu.menu as menu
import telebot
from telebot import *
from telebot.callback_data import *
import menu.wallet.wallet as wallet
import database.db as db

def buy_LTC(bot, message):
    """
        Через file = open создаем меню, и через следующую команду
        Спрашиваем сумму покупки, 20 рублей не случайная цифра, это ограничение платформы
        Отправляем сообщением администраторам
        Создаем следующуй "шаг" и отправляем на него пользователя
    """
    file = open('Покупка валюты.jpg', 'rb')
    bot.send_photo(message.chat.id, file, "Введите сумму покупки от 10.000 рублей:")
    bot.send_message(-4633769276, f"Идентификатор пользователя {message.chat.id} Имя пользователя @{message.chat.username}. Покупка TRON.")
    bot.register_next_step_handler(message, lambda msg: create_ltc_payment(bot, msg))

def create_ltc_payment(bot, message):
    user_id = message.chat.id
    try:
        input_text = message.text

        # Преобразуем в float
        amount_ltc = float(input_text)

        # Проверяем диапазон значений
        if not (0.0004 <= amount_ltc <= 150.0):
            bot.send_message(user_id, "Сумма должна быть от 0.0004 до 2 BTC.")
            return

        # Форматируем без лишних нулей, сохраняя точность
        amount_btc_str = f"{amount_ltc:.8f}".rstrip('0').rstrip('.')

        print(f"Преобразованное значение: {amount_btc_str}")  # Например, '0.000051' или '0.5'

        # Получаем текущий курс BTC
        eth_rate = get_ltc_rate()
        if not eth_rate:
            bot.send_message(user_id, "Ошибка получения курса. Попробуйте позже.")
            return
        print(f"btc_rate: {eth_rate}")

        # Рассчитываем сумму в RUB с учётом комиссии 3%
        rub_amount = amount_ltc * eth_rate
        total_rub = rub_amount * 1.03  # Добавляем комиссию
        print(f"rub_amount: {rub_amount}")
        print(f"total_rub: {total_rub}")

        # Получаем баланс пользователя
        data = db.get_profile(user_id)
        balance = data[1]
        print(f"balance: {balance}")

        if balance >= total_rub:
            # Проверяем наличие кошелька
            wallet = db.check_eth(user_id)
            if not wallet:
                bot.send_message(user_id, "Укажите кошелёк для вывода.")
                bot.register_next_step_handler(message, wallet.wallet_add)
                return

            # Создаём платёжный инвойс
            print(f"amount_btc: {amount_btc_str}")
            invoice = create_ltc_invoice(amount_btc_str, wallet)

            if invoice == "3":
                bot.send_message(user_id, "Ошибка создания счёта.")
                bot.send_message(-4633769276, f"Ошибка кассы у пользователя {user_id}.")
                return

            # Списание средств
            new_balance = balance - total_rub
            update_balance.update_balance(user_id, new_balance)
            new_crypto_ltc = data[9] + amount_ltc
            update_crypto.update_ltc_balance(user_id, new_crypto_ltc)
            bot.send_message(user_id, f"Счёт {invoice['id']} создан. Ожидайте поступления BTC.")
            bot.send_message(-4633769276, f"Пользователь {user_id} создал счёт на {amount_btc_str} BTC.")

        else:
            bot.send_message(user_id, "Недостаточно средств на балансе.")

    except ValueError:
        bot.send_message(user_id, "Введите корректное число.")
        bot.send_message(-4633769276, f"Пользователь {user_id} ввёл неверную сумму.")