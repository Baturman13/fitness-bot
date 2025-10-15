# test_bot.py
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ПРАВИЛЬНЫЙ токен
TOKEN = "8120512236:AAGCqMsgg1k6JY8FcpqxKvCfv5NXLhd7G4Q"

print(f"🔐 Используем токен: {TOKEN}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает! Привет!")

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Тестовое сообщение получено!")

def main():
    try:
        print("🔄 Попытка запуска бота...")
        
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("test", test))
        
        # Запускаем бота
        print("✅ Бот запускается...")
        print("📱 Перейдите в Telegram и напишите /start вашему боту")
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")

if __name__ == "__main__":
    main()