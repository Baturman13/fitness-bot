import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import database
import nutrition_parser

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Инициализация базы данных
db = database.Database()

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    update.message.reply_text(
        f"🏋️ Привет, {user.first_name}!\n\n"
        "Я FitnessBot - помогу тебе вести учет питания.\n\n"
        "Просто напиши что ты съел:\n"
        "• 'гречка 200г'\n" 
        "• 'яблоко 2 шт'\n"
        "• 'протеин 1 ложка'\n\n"
        "Доступные команды:\n"
        "/stats - статистика за сегодня\n"
        "/profile - настройка профиля"
    )
    
    # Сохраняем пользователя в БД
    db.add_user(
        user.id,
        user.username,
        user.first_name,
        user.last_name
    )

def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик текстовых сообщений"""
    try:
        user_id = update.effective_user.id
        text = update.message.text
        
        # Парсим питание
        result = nutrition_parser.parse_nutrition(text)
        
        if result:
            food_name, quantity, unit, nutrition = result
            
            # Сохраняем в БД
            db.save_meal(user_id, food_name, quantity, unit, nutrition)
            
            # Формируем ответ
            response = (
                f"✅ Добавлено:\n"
                f"🍽 {food_name} - {quantity}{unit}\n"
                f"📊 Калории: {nutrition['calories']} ккал\n"
                f"🥚 Белки: {nutrition['protein']}г\n"
                f"🥑 Жиры: {nutrition['fat']}г\n" 
                f"🍚 Углеводы: {nutrition['carbs']}г"
            )
        else:
            response = "❌ Не могу распознать продукт. Попробуйте другой формат, например: 'гречка 200г'"
            
        update.message.reply_text(response)
        
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        update.message.reply_text("❌ Произошла ошибка при обработке сообщения")

def stats_command(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /stats"""
    try:
        user_id = update.effective_user.id
        stats = db.get_user_stats(user_id, 1)  # Статистика за 1 день
        
        response = (
            f"📊 Статистика за сегодня:\n\n"
            f"🍽 Калории: {stats['total_calories']} ккал\n"
            f"🥚 Белки: {stats['total_protein']}г\n"
            f"🥑 Жиры: {stats['total_fat']}г\n"
            f"🍚 Углеводы: {stats['total_carbs']}г\n\n"
            f"📈 Приемов пищи: {stats['meal_count']}"
        )
        
        update.message.reply_text(response)
        
    except Exception as e:
        logging.error(f"Error getting stats: {e}")
        update.message.reply_text("❌ Ошибка при получении статистики")

def main():
    """Основная функция запуска бота"""
    token = os.getenv('TOKEN')
    if not token:
        logging.error("Токен не найден! Проверьте переменную окружения TOKEN")
        return

    # Создаем updater и dispatcher
    updater = Updater(token)
    dispatcher = updater.dispatcher

    # Регистрируем обработчики
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stats", stats_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запускаем бота
    logging.info("Бот запускается...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
