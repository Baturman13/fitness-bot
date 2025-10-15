# feedback.py
from datetime import datetime
import config
from telegram import Bot
import asyncio

class FeedbackSystem:
    def __init__(self, bot=None):
        self.bot = bot
    
    def set_bot(self, bot):
        self.bot = bot
    
    def add_feedback(self, user_id, message):
        print(f"📝 Отзыв от пользователя {user_id}: {message}")
        
        # Отправляем отзыв в канал (асинхронно)
        if self.bot and config.FEEDBACK_CHANNEL:
            asyncio.create_task(self.send_to_feedback_channel(user_id, message))
        
        if config.TEST_MODE:
            self.notify_test_mode(user_id)
    
    async def send_to_feedback_channel(self, user_id, message):
        try:
            feedback_text = (
                f"📢 <b>Новый отзыв</b>\n\n"
                f"👤 Пользователь: {user_id}\n"
                f"📅 Время: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                f"💬 <b>Сообщение:</b>\n{message}"
            )
            
            await self.bot.send_message(
                chat_id=config.FEEDBACK_CHANNEL,
                text=feedback_text,
                parse_mode='HTML'
            )
            print(f"✅ Отзыв отправлен в канал {config.FEEDBACK_CHANNEL}")
            
        except Exception as e:
            print(f"❌ Ошибка отправки отзыва в канал: {e}")
    
    def notify_test_mode(self, user_id):
        print(f"🔔 Уведомление для {user_id}: Бот в тестовом режиме")