import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def start(update, context):
    update.message.reply_text(
        "🏋️ FitnessBot запущен!\n\n"
        "Теперь я буду работать 24/7!\n"
        "Пишите что вы съели, например:\n"
        "• гречка 200г\n"
        "• яблоко 2 шт\n"
        "• протеин 1 ложка"
    )

def handle_message(update, context):
    text = update.message.text
    update.message.reply_text(f"✅ Записал: {text}")

def main():
    token = os.getenv('TOKEN')
    if not token:
        logging.error("Токен не найден!")
        return

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    logging.info("🚀 Бот запускается...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
