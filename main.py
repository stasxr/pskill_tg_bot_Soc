import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Telegram API токен
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# Команда для завершения процесса
def kill_process(update: Update, context: CallbackContext) -> None:
    if len(context.args) < 2:
        update.message.reply_text("Используйте команду в формате: /kill <имя_или_PID_процесса> <IP_адрес_ПК>")
        return

    process_name_or_pid = context.args[0]  # Имя или PID процесса
    remote_ip = context.args[1]  # IP-адрес удаленного ПК

    # Формируем команду для pskill
    pskill_command = f"pskill \\\\{remote_ip} -u <админ_пользователь> -p <пароль> {process_name_or_pid}"

    try:
        # Выполняем команду pskill
        result = subprocess.run(pskill_command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            update.message.reply_text(f"Процесс {process_name_or_pid} на {remote_ip} успешно завершён.")
        else:
            update.message.reply_text(f"Ошибка при завершении процесса: {result.stderr}")
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка: {e}")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Команда для завершения процесса
    dispatcher.add_handler(CommandHandler("kill", kill_process))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
