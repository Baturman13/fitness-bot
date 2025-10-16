import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    await update.message.reply_text("✅ Бот работает! Фитнес-трекер запущен.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Эхо-ответ для тестирования"""
    await update.message.reply_text(f"Получил: {update.message.text}")

def main():
    """Запуск бота"""
    token = os.getenv('TOKEN')
    if not token:
        logging.error("Токен не найден!")
        return

    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем
    logging.info("Бот запускается...")
    application.run_polling()

if __name__ == '__main__':
    main()
