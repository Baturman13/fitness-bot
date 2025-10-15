# bot.py
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import config
import database
import nutrition_parser
import feedback
import recommendations
import dialog_system

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
AGE, GENDER, HEIGHT, WEIGHT, TARGET_WEIGHT, ACTIVITY, GOAL = range(7)

class FitnessBot:
    def __init__(self):
        self.db = database.Database()
        self.parser = nutrition_parser.NutritionParser()
        self.feedback_system = feedback.FeedbackSystem()
        self.recommendation_system = recommendations.RecommendationSystem()
        self.dialog_system = dialog_system.DialogSystem()
        # Оставляем только для создания профиля
        self.user_last_messages = {}
        self.user_temp_data = {}
    
    def set_bot(self, bot):
        self.feedback_system.set_bot(bot)
        self.bot = bot
    
    # Методы для создания профиля (удаление сообщений оставлено только здесь)
    async def delete_previous_message(self, user_id, chat_id):
        if user_id in self.user_last_messages:
            try:
                message_id = self.user_last_messages[user_id]
                await self.bot.delete_message(chat_id=chat_id, message_id=message_id)
                del self.user_last_messages[user_id]
            except Exception:
                pass
    
    async def send_message_and_save_id(self, chat_id, user_id, text, **kwargs):
        await self.delete_previous_message(user_id, chat_id)
        message = await self.bot.send_message(chat_id=chat_id, text=text, **kwargs)
        self.user_last_messages[user_id] = message.message_id
        return message

    # ОСНОВНЫЕ КОМАНДЫ
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.db.add_user(user.id, user.first_name)
        
        welcome_text = (
            f"👋 <b>Привет, {user.first_name}!</b>\n\n"
            
            "🎯 <b>Добро пожаловать в умный FitnessBot!</b>\n"
            "Я ваш персональный фитнес-помощник с расширенными возможностями:\n\n"
            
            "🍽️ <b>Умный учет питания:</b>\n"
            "• 800+ продуктов, блюд и напитков\n"
            "• Алкогольные напитки\n"
            "• Спортивные добавки\n"
            "• Лекарства и витамины\n"
            "• Бытовые меры: тарелки, стаканы, ложки\n\n"
            
            "💬 <b>Диалоговый режим:</b>\n"
            "• Задавайте любые вопросы о питании\n"
            "• Советы по тренировкам\n"
            "• Информация о добавках\n"
            "• Рекомендации по прогрессу\n\n"
            
            "📊 <b>Расширенная статистика:</b>\n"
            "• Статистика за разные периоды\n"
            "• Анализ прогресса\n"
            "• Самые частые продукты\n\n"
            
            "🚀 <b>Как начать:</b>\n"
            "• Напишите что съели: 'гречка тарелка' или 'протеин 2 ложки'\n"
            "• Или задайте вопрос: 'как похудеть?'\n"
            "• Или используйте команды ниже\n\n"
            
            "📝 <b>Основные команды:</b>\n"
            "/profile - создать персональный профиль\n"
            "/stats - статистика питания\n"
            "/analysis - анализ питания\n"
            "/advice - персональные рекомендации\n"
            "/training - советы по тренировкам\n"
            "/supplements - информация о добавках\n"
            "/progress - отслеживание прогресса\n"
            "/help - помощь\n\n"
            
            "🧪 <b>Бот в тестовом режиме</b>\n"
            "Все функции бесплатны! Помогите нам стать лучше 💬"
        )
        
        await update.message.reply_text(welcome_text, parse_mode='HTML')
        
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = (
            "📖 <b>Помощь по использованию FitnessBot</b>\n\n"
            
            "🍽️ <b>Добавление еды (новые возможности):</b>\n"
            "• 'гречка тарелка' - готовые блюда\n"
            "• 'протеин 2 ложки' - спортивные добавки\n"
            "• 'пиво бутылка' - алкогольные напитки\n"
            "• 'витамины 1 шт' - лекарства и витамины\n"
            "• 'салат оливье порция' - сложные блюда\n\n"
            
            "💬 <b>Диалоговый режим:</b>\n"
            "Задавайте вопросы в свободной форме:\n"
            "• 'Как похудеть?'\n"
            "• 'Какие добавки принимать?'\n"
            "• 'Советы по тренировкам дома'\n"
            "• 'Что есть после тренировки?'\n\n"
            
            "📊 <b>Статистика:</b>\n"
            "/stats - за сегодня\n"
            "/stats 2days - за 2 дня\n"
            "/stats week - за неделю\n"
            "/stats month - за месяц\n"
            "/stats year - за год\n\n"
            
            "👤 <b>Профиль и аналитика:</b>\n"
            "/profile - создать/изменить профиль\n"
            "/analysis - анализ питания за период\n"
            "/advice - персональные рекомендации\n"
            "/training - советы по тренировкам\n"
            "/supplements - информация о добавках\n"
            "/progress - анализ прогресса\n\n"
            
            "💡 <b>Совет:</b> Начните с заполнения профиля командой /profile"
        )
        
        await update.message.reply_text(help_text, parse_mode='HTML')

    # СИСТЕМА ПРОФИЛЯ (оставляем без изменений)
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        existing_profile = self.db.get_user_profile(user.id)
        
        if existing_profile:
            profile_text = (
                f"👤 <b>Ваш текущий профиль:</b>\n\n"
                f"📅 Возраст: {existing_profile.get('age', 'Не указан')}\n"
                f"⚧ Пол: {existing_profile.get('gender', 'Не указан')}\n"
                f"📏 Рост: {existing_profile.get('height', 'Не указан')} см\n"
                f"⚖️ Вес: {existing_profile.get('weight', 'Не указан')} кг\n"
                f"🎯 Целевой вес: {existing_profile.get('target_weight', 'Не указан')} кг\n"
                f"🏃 Активность: {existing_profile.get('activity_level', 'Не указана')}\n"
                f"📈 Цель: {existing_profile.get('goal', 'Не указана')}\n\n"
                f"Хотите изменить профиль? Напишите /profile"
            )
            await update.message.reply_text(profile_text, parse_mode='HTML')
        else:
            await self.start_profile_creation(update, context)
    
    async def start_profile_creation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        self.user_temp_data[user.id] = {}
        
        text = (
            "👤 <b>Создание профиля</b>\n\n"
            "Для персональных рекомендаций мне нужно узнать немного о вас.\n\n"
            "📅 <b>Шаг 1 из 7: Укажите ваш возраст</b>\n"
            "Например: <i>25</i>"
        )
        
        await self.send_message_and_save_id(update.effective_chat.id, user.id, text, parse_mode='HTML')
        return AGE
    
    async def get_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        try:
            age = int(update.message.text)
            if age < 10 or age > 100:
                await update.message.reply_text("❌ Пожалуйста, укажите реальный возраст (10-100 лет)")
                return AGE
            
            self.user_temp_data[user.id]['age'] = age
            
            keyboard = [['Мужской', 'Женский']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            
            text = (
                "✅ Возраст сохранен!\n\n"
                "⚧ <b>Шаг 2 из 7: Укажите ваш пол</b>"
            )
            
            await self.send_message_and_save_id(update.effective_chat.id, user.id, text, parse_mode='HTML')
            await update.message.reply_text("Выберите пол:", reply_markup=reply_markup)
            return GENDER
            
        except ValueError:
            await update.message.reply_text("❌ Пожалуйста, укажите возраст числом")
            return AGE
    
    async def get_gender(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        gender = update.message.text.lower()
        
        if gender in ['мужской', 'женский']:
            self.user_temp_data[user.id]['gender'] = 'male' if gender == 'мужской' else 'female'
            
            text = (
                "✅ Пол сохранен!\n\n"
                "📏 <b>Шаг 3 из 7: Укажите ваш рост в см</b>\n"
                "Например: <i>175</i>"
            )
            
            await self.send_message_and_save_id(update.effective_chat.id, user.id, text, parse_mode='HTML')
            await update.message.reply_text("Укажите рост:", reply_markup=ReplyKeyboardRemove())
            return HEIGHT
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите пол из предложенных вариантов")
            return GENDER
    
    async def get_height(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        try:
            height = float(update.message.text)
            if height < 100 or height > 250:
                await update.message.reply_text("❌ Пожалуйста, укажите реальный рост (100-250 см)")
                return HEIGHT
            
            self.user_temp_data[user.id]['height'] = height
            
            text = (
                "✅ Рост сохранен!\n\n"
                "⚖️ <b>Шаг 4 из 7: Укажите ваш текущий вес в кг</b>\n"
                "Например: <i>70.5</i>"
            )
            
            await self.send_message_and_save_id(update.effective_chat.id, user.id, text, parse_mode='HTML')
            return WEIGHT
            
        except ValueError:
            await update.message.reply_text("❌ Пожалуйста, укажите рост числом")
            return HEIGHT
    
    async def get_weight(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        try:
            weight = float(update.message.text)
            if weight < 30 or weight > 300:
                await update.message.reply_text("❌ Пожалуйста, укажите реальный вес (30-300 кг)")
                return WEIGHT
            
            self.user_temp_data[user.id]['weight'] = weight
            
            text = (
                "✅ Вес сохранен!\n\n"
                "🎯 <b>Шаг 5 из 7: Укажите ваш желаемый вес в кг</b>\n"
                "Например: <i>65</i>"
            )
            
            await self.send_message_and_save_id(update.effective_chat.id, user.id, text, parse_mode='HTML')
            return TARGET_WEIGHT
            
        except ValueError:
            await update.message.reply_text("❌ Пожалуйста, укажите вес числом")
            return WEIGHT
    
    async def get_target_weight(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        try:
            target_weight = float(update.message.text)
            if target_weight < 30 or target_weight > 300:
                await update.message.reply_text("❌ Пожалуйста, укажите реальный целевой вес (30-300 кг)")
                return TARGET_WEIGHT
            
            self.user_temp_data[user.id]['target_weight'] = target_weight
            
            keyboard = [['Низкая', 'Средняя', 'Высокая', 'Очень высокая']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            
            text = (
                "✅ Целевой вес сохранен!\n\n"
                "🏃 <b>Шаг 6 из 7: Укажите уровень активности</b>\n\n"
                "• Низкая - сидячая работа, нет тренировок\n"
                "• Средняя - легкие тренировки 1-3 раза/неделю\n"
                "• Высокая - тренировки 3-5 раз/неделю\n"
                "• Очень высокая - ежедневные интенсивные тренировки"
            )
            
            await self.send_message_and_save_id(update.effective_chat.id, user.id, text, parse_mode='HTML')
            await update.message.reply_text("Выберите уровень активности:", reply_markup=reply_markup)
            return ACTIVITY
            
        except ValueError:
            await update.message.reply_text("❌ Пожалуйста, укажите вес числом")
            return TARGET_WEIGHT
    
    async def get_activity(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        activity = update.message.text.lower()
        
        activity_map = {
            'низкая': 'sedentary',
            'средняя': 'moderate', 
            'высокая': 'active',
            'очень высокая': 'very_active'
        }
        
        if activity in activity_map:
            self.user_temp_data[user.id]['activity_level'] = activity_map[activity]
            
            keyboard = [['Похудение', 'Поддержание', 'Набор массы']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            
            text = (
                "✅ Уровень активности сохранен!\n\n"
                "📈 <b>Шаг 7 из 7: Выберите вашу цель</b>"
            )
            
            await self.send_message_and_save_id(update.effective_chat.id, user.id, text, parse_mode='HTML')
            await update.message.reply_text("Выберите цель:", reply_markup=reply_markup)
            return GOAL
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите уровень активности из предложенных вариантов")
            return ACTIVITY
    
    async def get_goal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        goal = update.message.text.lower()
        
        goal_map = {
            'похудение': 'lose',
            'поддержание': 'maintain', 
            'набор массы': 'gain'
        }
        
        if goal in goal_map:
            self.user_temp_data[user.id]['goal'] = goal_map[goal]
            
            # Сохраняем профиль
            profile_data = self.user_temp_data[user.id]
            
            # Рассчитываем суточные потребности
            daily_needs = self.recommendation_system.calculate_daily_needs(profile_data)
            if daily_needs:
                profile_data.update(daily_needs)
            
            self.db.save_user_profile(user.id, profile_data)
            
            # Очищаем временные данные
            del self.user_temp_data[user.id]
            
            text = (
                "🎉 <b>Профиль успешно создан!</b>\n\n"
                f"📊 <b>Ваши суточные потребности:</b>\n"
                f"🔥 Калории: {daily_needs['daily_calories']} ккал/день\n"
                f"⚖️ Белки: {daily_needs['daily_protein']}г\n"
                f"🥑 Жиры: {daily_needs['daily_fat']}г\n"
                f"🍚 Углеводы: {daily_needs['daily_carbs']}г\n\n"
                "Теперь вы можете получать персональные рекомендации!\n"
                "Используйте /advice для получения советов"
            )
            
            await self.send_message_and_save_id(update.effective_chat.id, user.id, text, parse_mode='HTML')
            await update.message.reply_text("Профиль сохранен!", reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END
        else:
            await update.message.reply_text("❌ Пожалуйста, выберите цель из предложенных вариантов")
            return GOAL
    
    async def cancel_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if user.id in self.user_temp_data:
            del self.user_temp_data[user.id]
        
        await self.send_message_and_save_id(update.effective_chat.id, user.id, "❌ Создание профиля отменено", parse_mode='HTML')
        await update.message.reply_text("Создание профиля отменено", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    # КОМАНДА ДОБАВОК
    async def supplements_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        supplements_text = (
            "🧪 <b>Спортивные добавки и лекарства</b>\n\n"
            
            "💪 <b>Основные добавки:</b>\n"
            "• Протеин - рост и восстановление мышц\n"
            "• Креатин - увеличение силы\n"
            "• BCAA - защита мышц во время тренировки\n"
            "• Гейнер - набор массы\n"
            "• L-карнитин - жиросжигание\n"
            "• Омега-3 - здоровье суставов и сердца\n\n"
            
            "💊 <b>Лекарства и витамины:</b>\n"
            "• Витамин D - иммунитет и настроение\n"
            "• Магний - расслабление и сон\n"
            "• Цинк - тестостерон и иммунитет\n"
            "• Мелатонин - качественный сон\n\n"
            
            "📝 <b>Как добавить в дневник:</b>\n"
            "Напишите: 'протеин 30г' или 'витамины 1 шт'\n\n"
            
            "⚠️ <b>Важно:</b> Перед приемом добавок проконсультируйтесь с врачом!"
        )
        
        await update.message.reply_text(supplements_text, parse_mode='HTML')

    # АНАЛИТИКА И РЕКОМЕНДАЦИИ
    async def analysis_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        # Анализ за 7 дней
        analytics = self.db.get_period_stats(user.id, days=7)
        
        analysis_text = (
            f"📊 <b>Анализ питания за 7 дней</b>\n\n"
            f"📅 Дней с записями: {analytics['days_count']}\n"
            f"🍽 Всего приемов пищи: {analytics['meal_count']}\n"
            f"🔥 Съедено калорий: {analytics['total_calories']}\n"
            f"⚖️ Белки: {analytics['total_protein']}г\n"
            f"🥑 Жиры: {analytics['total_fat']}г\n"
            f"🍚 Углеводы: {analytics['total_carbs']}г\n"
            f"📈 Среднедневные калории: {analytics['avg_daily_calories']}\n\n"
        )
        
        # Самые частые продукты
        if analytics['common_foods']:
            analysis_text += "🍎 <b>Самые частые продукты:</b>\n"
            for i, (product, count, weight) in enumerate(analytics['common_foods'], 1):
                analysis_text += f"{i}. {product}: {count} раз\n"
        
        await update.message.reply_text(analysis_text, parse_mode='HTML')
    
    async def advice_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        profile = self.db.get_user_profile(user.id)
        analytics = self.db.get_period_stats(user.id, days=7)
        
        if not profile:
            text = (
                "❌ <b>Профиль не найден</b>\n\n"
                "Для получения персональных рекомендаций необходимо создать профиль.\n"
                "Используйте команду /profile"
            )
            await update.message.reply_text(text, parse_mode='HTML')
            return
        
        recommendations_list = self.recommendation_system.generate_nutrition_recommendations(profile, analytics)
        
        advice_text = "💡 <b>Персональные рекомендации по питанию</b>\n\n"
        for i, recommendation in enumerate(recommendations_list, 1):
            advice_text += f"{i}. {recommendation}\n"
        
        await update.message.reply_text(advice_text, parse_mode='HTML')
    
    async def training_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        profile = self.db.get_user_profile(user.id)
        
        if not profile:
            text = (
                "❌ <b>Профиль не найден</b>\n\n"
                "Для получения тренировочных рекомендаций необходимо создать профиль.\n"
                "Используйте команду /profile"
            )
            await update.message.reply_text(text, parse_mode='HTML')
            return
        
        recommendations_list = self.recommendation_system.generate_training_recommendations(profile)
        
        training_text = "💪 <b>Рекомендации по тренировкам</b>\n\n"
        for i, recommendation in enumerate(recommendations_list, 1):
            training_text += f"{i}. {recommendation}\n"
        
        await update.message.reply_text(training_text, parse_mode='HTML')
    
    async def progress_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        profile = self.db.get_user_profile(user.id)
        analytics = self.db.get_period_stats(user.id, days=30)
        
        if not profile:
            text = (
                "❌ <b>Профиль не найден</b>\n\n"
                "Для анализа прогресса необходимо создать профиль.\n"
                "Используйте команду /profile"
            )
            await update.message.reply_text(text, parse_mode='HTML')
            return
        
        progress_analysis = self.recommendation_system.get_progress_analysis(profile, analytics)
        
        progress_text = (
            f"📈 <b>Анализ вашего прогресса</b>\n\n"
            f"{progress_analysis}\n\n"
            f"📊 <b>Статистика за 30 дней:</b>\n"
            f"• Среднедневные калории: {analytics['avg_daily_calories']}\n"
            f"• Всего приемов пищи: {analytics['meal_count']}\n"
            f"• Дней с записями: {analytics['days_count']}\n\n"
            f"💪 Продолжайте работу над собой!"
        )
        
        await update.message.reply_text(progress_text, parse_mode='HTML')

    # ИСПРАВЛЕННАЯ ОБРАБОТКА СООБЩЕНИЙ
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        text = update.message.text.strip()
        
        print(f"🔄 Получено сообщение от {user.first_name}: '{text}'")
        
        # Сначала проверяем, является ли сообщение вводом еды
        is_food = self.parser.is_food_input(text)
        print(f"🍽️ Это еда? {is_food}")
        
        if is_food:
            print("✅ Распознано как еда")
            nutrition_data = self.parser.parse_input(text)
            
            if nutrition_data:
                print(f"📊 Данные еды: {nutrition_data}")
                # Сохраняем в базу
                success = self.db.add_meal(user_id, nutrition_data)
                if success:
                    print("✅ Данные сохранены в базу")
                else:
                    print("❌ Ошибка сохранения в базу")
                
                # Дополнительная информация для добавок и лекарств
                extra_info = ""
                if nutrition_data['type'] == 'добавка':
                    supplement_info = self.parser.get_supplement_info(nutrition_data['product'])
                    extra_info = f"\n💡 {supplement_info}"
                elif nutrition_data['type'] == 'лекарство':
                    extra_info = "\n⚠️ Не забывайте принимать по инструкции!"
                elif nutrition_data['type'] == 'алкоголь':
                    extra_info = "\n🍷 Учитывайте в дневной норме калорий"
                
                response = (
                    f"✅ <b>Записал прием пищи:</b>\n"
                    f"🍽 {nutrition_data['product']} - {nutrition_data['weight']}г\n"
                    f"🔥 ~{nutrition_data['calories']} ккал\n"
                    f"⚖️ Белки: {nutrition_data['protein']}г\n"
                    f"🥑 Жиры: {nutrition_data['fat']}г\n"
                    f"🍚 Углеводы: {nutrition_data['carbs']}г"
                    f"{extra_info}"
                )
                await update.message.reply_text(response, parse_mode='HTML')
                print("📨 Ответ отправлен пользователю")
            else:
                # ЕСЛИ ПРОДУКТ НЕ НАЙДЕН - ЧЕТКО СООБЩАЕМ
                print(f"❌ Не удалось распарсить: '{text}'")
                response = (
                    "❌ <b>Не удалось распознать продукт</b>\n\n"
                    "Возможные причины:\n"
                    "• Продукта нет в моей базе данных\n" 
                    "• Неправильный формат ввода\n\n"
                    "💡 <b>Попробуйте так:</b>\n"
                    "• 'гречка тарелка'\n"
                    "• 'яблоко 2 шт'\n"
                    "• 'протеин 30г'\n\n"
                    f"<i>Отладка: '{text}'</i>"
                )
                await update.message.reply_text(response, parse_mode='HTML')
        else:
            # Если это не еда, то обрабатываем как диалог
            print("💬 Распознано как диалог")
            profile = self.db.get_user_profile(user_id)
            response = self.dialog_system.generate_response(text, profile)
            await update.message.reply_text(response, parse_mode='HTML')

    # РАСШИРЕННАЯ СТАТИСТИКА С ВЫБОРОМ ПЕРИОДА
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
        # Определяем период из аргументов команды
        period = context.args[0] if context.args else 'today'
        
        if period == 'today':
            stats = self.db.get_daily_stats(user_id)
            period_text = stats.get('period', 'сегодня')
        elif period == '2days':
            stats = self.db.get_period_stats(user_id, days=2)
            period_text = stats['period']
        elif period == 'week':
            stats = self.db.get_period_stats(user_id, days=7)
            period_text = stats['period']
        elif period == 'month':
            stats = self.db.get_period_stats(user_id, days=30)
            period_text = stats['period']
        elif period == 'year':
            stats = self.db.get_monthly_stats(user_id, months=12)
            period_text = stats['period']
        else:
            stats = self.db.get_daily_stats(user_id)
            period_text = stats.get('period', 'сегодня')
        
        # Формируем текст статистики
        stats_text = (
            f"📊 <b>Статистика питания</b>\n"
            f"⏰ Период: <i>{period_text}</i>\n\n"
            f"🍽 Приемов пищи: {stats['meal_count']}\n"
            f"🔥 Калории: {stats['total_calories']} ккал\n"
            f"⚖️ Белки: {stats['total_protein']}г\n"
            f"🥑 Жиры: {stats['total_fat']}г\n"
            f"🍚 Углеводы: {stats['total_carbs']}г\n"
        )
        
        # Добавляем средние значения для периодов больше 1 дня
        if 'avg_daily_calories' in stats and stats['avg_daily_calories'] > 0:
            stats_text += f"📈 Среднедневные калории: {stats['avg_daily_calories']} ккал\n"
        
        # Добавляем информацию о самых частых продуктах
        if 'common_foods' in stats and stats['common_foods']:
            stats_text += f"\n🍎 <b>Самые частые продукты:</b>\n"
            for i, (product, count, weight) in enumerate(stats['common_foods'], 1):
                stats_text += f"{i}. {product}: {count} раз\n"
        
        # Добавляем подсказку по выбору периода
        stats_text += (
            f"\n💡 <b>Выберите период:</b>\n"
            f"/stats today - за сегодня\n"
            f"/stats 2days - за 2 дня\n" 
            f"/stats week - за неделю\n"
            f"/stats month - за месяц\n"
            f"/stats year - за год"
        )
        
        await update.message.reply_text(stats_text, parse_mode='HTML')
    
    async def handle_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        
        if context.args:
            feedback_text = " ".join(context.args)
            self.feedback_system.add_feedback(user.id, feedback_text)
            
            response = (
                "✅ <b>Спасибо за ваш отзыв!</b>\n\n"
                "Мы очень ценим ваше мнение и обязательно рассмотрим ваше предложение. "
                "Вместе мы сделаем бота лучше! 🚀\n\n"
                "Если у вас есть еще идеи - просто напишите их командой /feedback"
            )
            await update.message.reply_text(response, parse_mode='HTML')
        else:
            help_text = (
                "💡 <b>Поделитесь вашим мнением!</b>\n\n"
                "Расскажите, что вам нравится, а что можно улучшить. "
                "Мы читаем все отзывы и используем их для развития бота.\n\n"
                "✍️ <b>Как оставить отзыв:</b>\n"
                "Напишите <code>/feedback ваш текст</code>\n\n"
                "Например: <code>/feedback Добавьте пожалуйста функцию напоминаний о воде</code>"
            )
            await update.message.reply_text(help_text, parse_mode='HTML')

def main():
    try:
        print("🔄 Инициализация улучшенного бота...")
        bot = FitnessBot()
        
        application = Application.builder().token(config.TOKEN).build()
        bot.set_bot(application.bot)
        
        # ConversationHandler для создания профиля
        profile_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('profile', bot.start_profile_creation)],
            states={
                AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_age)],
                GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_gender)],
                HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_height)],
                WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_weight)],
                TARGET_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_target_weight)],
                ACTIVITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_activity)],
                GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_goal)],
            },
            fallbacks=[CommandHandler('cancel', bot.cancel_profile)]
        )
        
        # Добавляем обработчики
        application.add_handler(CommandHandler("start", bot.start))
        application.add_handler(CommandHandler("help", bot.help_command))
        application.add_handler(CommandHandler("stats", bot.show_stats))
        application.add_handler(CommandHandler("feedback", bot.handle_feedback))
        application.add_handler(CommandHandler("analysis", bot.analysis_command))
        application.add_handler(CommandHandler("advice", bot.advice_command))
        application.add_handler(CommandHandler("training", bot.training_command))
        application.add_handler(CommandHandler("supplements", bot.supplements_command))
        application.add_handler(CommandHandler("progress", bot.progress_command))
        application.add_handler(profile_conv_handler)
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
        
        print("🤖 Улучшенный бот запущен...")
        print("🌐 Режим: Локальный (VS Code)")
        print("📊 Доступна расширенная статистика!")
        print("🍽️ База: 800+ продуктов и напитков")
        
        # ЗАПУСК ДЛЯ ЛОКАЛЬНОЙ РАБОТЫ
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")

if __name__ == "__main__":
    main()