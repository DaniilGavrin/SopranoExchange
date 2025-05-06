"""
    Импортируем настройки
"""
import settings

def change_admin(bot, message):
    """
        Функция изменения администратора
        Принимаем в качестве сообщения id пользователя для смены администратора,
    """
    bot.send_message(-4633769276, "Запущена функция изменения администратора администратором.")
    bot.send_message(message.chat.id, "Введите пожалуйста новый id администратора или cancel для отмены")
    bot.register_next_step_handler(message, lambda msg: change_admin_new_id(bot,msg))


def change_admin_new_id(bot, message):
    """
        Функция изменения нового администратора
        Принимаем в качестве сообщения новый id администратора.
        В случаи отмены соглащаемся на отмену
        В случаи ввода корректных данных, сохраняем нового администратора в параметр настроек и отправляем сообщение об успешном изменении
    """
    msg = message.text
    if msg == "cancel":
        bot.send_message(message.chat.id, "Изменение отменено.")
        bot.send_message(-4633769276, "Изменение отменено администратором")
    else:
        try:
            new_admin_id = msg
            settings.ADMIN_USER = new_admin_id
            bot.send_message(message.chat.id, f"Администратор изменен на id {new_admin_id}")
            bot.send_message(-4633769276, f"Администратор изменен на id {new_admin_id}")
        except ValueError:
            bot.send_message(message.chat.id, "Введите корректные данные")
            bot.send_message(-4633769276, "Возникла ошибка при изменении администратора")