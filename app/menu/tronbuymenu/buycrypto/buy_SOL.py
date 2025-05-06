from database import update_balance, update_crypto
from kassa.kassa import create_sol_invoice
from course.SOL import get_sol_rate
import menu.menu as menu
import telebot
from telebot import *
from telebot.callback_data import *
import menu.wallet.wallet as wallet
import database.db as db

def buy_SOL(bot, message):
    """
        Через file = open создаем меню, и через следующую команду
        Спрашиваем сумму покупки, 20 рублей не случайная цифра, это ограничение платформы
        Отправляем сообщением администраторам
        Создаем следующуй "шаг" и отправляем на него пользователя
    """
    file = open('Покупка валюты.jpg', 'rb')
    bot.send_photo(message.chat.id, file, "Введите сумму покупки от 20 рублей:")
    bot.send_message(-4633769276, f"Идентификатор пользователя {message.chat.id} Имя пользователя @{message.chat.username}. Покупка TRON.")
    bot.register_next_step_handler(message, lambda msg: create_sol_payment(bot, msg))

def create_sol_payment(bot, message):
    user_id = message.chat.id
    try:
        input_text = message.text

        # Преобразуем в float
        amount_sol = float(input_text)

        # Проверяем диапазон значений
        if not (0.00127 <= amount_sol <= 1000.0):
            bot.send_message(user_id, "Сумма должна быть от 0.00127 до 1000 SOL.")
            return

        # Форматируем без лишних нулей, сохраняя точность
        amount_sol_str = f"{amount_sol:.8f}".rstrip('0').rstrip('.')

        print(f"Преобразованное значение: {amount_sol_str}")  # Например, '0.000051' или '0.5'

        # Получаем текущий курс BTC
        sol_rate = get_sol_rate()
        if not sol_rate:
            bot.send_message(user_id, "Ошибка получения курса. Попробуйте позже.")
            return
        print(f"btc_rate: {sol_rate}")

        # Рассчитываем сумму в RUB с учётом комиссии 3%
        rub_amount = amount_sol * sol_rate
        total_rub = rub_amount * 1.03  # Добавляем комиссию
        print(f"rub_amount: {rub_amount}")
        print(f"total_rub: {total_rub}")

        # Получаем баланс пользователя
        data = db.get_profile(user_id)
        balance = data[1]
        print(f"balance: {balance}")

        if balance >= total_rub:
            # Проверяем наличие кошелька
            wallet = db.check_sol(user_id)
            if not wallet:
                bot.send_message(user_id, "Укажите кошелёк для вывода.")
                bot.register_next_step_handler(message, wallet.wallet_add)
                return

            # Создаём платёжный инвойс
            print(f"amount_btc: {amount_sol_str}")
            invoice = create_sol_invoice(amount_sol_str, wallet)

            if invoice == "3":
                bot.send_message(user_id, "Ошибка создания счёта.")
                bot.send_message(-4633769276, f"Ошибка кассы у пользователя {user_id}.")
                return

            # Списание средств
            new_balance = balance - total_rub
            update_balance.update_balance(user_id, new_balance)
            new_crypto_sol = data[11] + amount_sol
            update_crypto.update_sol_balance(user_id, new_crypto_sol)
            bot.send_message(user_id, f"Счёт {invoice['id']} создан. Ожидайте поступления BTC.")
            bot.send_message(-4633769276, f"Пользователь {user_id} создал счёт на {amount_sol_str} BTC.")

        else:
            bot.send_message(user_id, "Недостаточно средств на балансе.")

    except ValueError:
        bot.send_message(user_id, "Введите корректное число.")
        bot.send_message(-4633769276, f"Пользователь {user_id} ввёл неверную сумму.")