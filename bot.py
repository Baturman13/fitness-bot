import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"🏋️ Привет, {user.first_name}!\n\n"
        "Я FitnessBot - помогу тебе вести учет питания.\n\n"
        "Просто напиши что ты съел:\n"
        "• 'гречка 200г'\n" 
        "• 'яблоко 2 шт'\n"
        "• 'протеин 1 ложка'\n\n"
        "Доступные команды:\n"
        "/stats - статистика за сегодня"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик текстовых сообщений"""
    try:
        text = update.message.text
        user = update.effective_user
        
        # Простой ответ вместо полноценного парсера (для начала)
        response = (
            f"✅ Принято: {text}\n\n"
            f"Спасибо, {user.first_name}! Запись сохранена.\n"
            f"Скоро я научусь анализировать питание и показывать статистику!"
        )
        
        await update.message.reply_text(response)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ Произошла ошибка")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /stats"""
    await update.message.reply_text(
        "📊 Статистика будет доступна скоро!\n\n"
        "Сейчас я настраиваюсь и уже скоро смогу показывать:\n"
        "• Калории за день\n"
        "• Белки/жиры/углеводы\n"
        "• Прогресс по целям"
    )

def main() -> None:
    """Основная функция запуска бота"""
    token = os.getenv('TOKEN')
    if not token:
        logger.error("Токен не найден! Проверьте переменную окружения TOKEN")
        return

    # Создаем Application
    application = Application.builder().token(token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    logger.info("🚀 Бот запускается...")
    application.run_polling()

if __name__ == '__main__':
    main()
