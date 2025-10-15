# database.py
import sqlite3
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_path='fitness_bot.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица профилей пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                age INTEGER,
                gender TEXT,
                height REAL,
                weight REAL,
                target_weight REAL,
                activity_level TEXT,
                goal TEXT,
                daily_calories INTEGER,
                daily_protein REAL,
                daily_fat REAL,
                daily_carbs REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица приемов пищи
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product TEXT,
                weight REAL,
                calories REAL,
                protein REAL,
                fat REAL,
                carbs REAL,
                type TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица отзывов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                feedback_text TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        self.conn.commit()

    def add_user(self, user_id, username):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username)
                VALUES (?, ?)
            ''', (user_id, username))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")

    def save_user_profile(self, user_id, profile_data):
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO user_profiles 
                (user_id, age, gender, height, weight, target_weight, activity_level, goal, daily_calories, daily_protein, daily_fat, daily_carbs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                profile_data.get('age'),
                profile_data.get('gender'),
                profile_data.get('height'),
                profile_data.get('weight'),
                profile_data.get('target_weight'),
                profile_data.get('activity_level'),
                profile_data.get('goal'),
                profile_data.get('daily_calories'),
                profile_data.get('daily_protein'),
                profile_data.get('daily_fat'),
                profile_data.get('daily_carbs')
            ))
            self.conn.commit()
        except Exception as e:
            print(f"Ошибка сохранения профиля: {e}")

    def get_user_profile(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        if row:
            columns = [description[0] for description in cursor.description]
            return dict(zip(columns, row))
        return None

    def add_meal(self, user_id, nutrition_data):
        """Добавляет прием пищи в базу данных"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO meals (user_id, product, weight, calories, protein, fat, carbs, type, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            ''', (user_id, nutrition_data['product'], nutrition_data['weight'], 
                  nutrition_data['calories'], nutrition_data['protein'], 
                  nutrition_data['fat'], nutrition_data['carbs'], nutrition_data['type']))
            self.conn.commit()
            print(f"✅ Прием пищи добавлен для пользователя {user_id}")
            return True
        except Exception as e:
            print(f"❌ Ошибка добавления приема пищи: {e}")
            return False

    def get_daily_stats(self, user_id, date=None):
        """Получает статистику за сегодняшний день - ИСПРАВЛЕННАЯ ВЕРСИЯ"""
        cursor = self.conn.cursor()
        
        # Используем CURRENT_DATE вместо DATE('now') для совместимости
        cursor.execute('''
            SELECT 
                COUNT(*) as meal_count,
                SUM(calories) as total_calories,
                SUM(protein) as total_protein,
                SUM(fat) as total_fat,
                SUM(carbs) as total_carbs
            FROM meals 
            WHERE user_id = ? AND DATE(timestamp) = CURRENT_DATE
        ''', (user_id,))
        
        row = cursor.fetchone()
        print(f"📊 Результат запроса статистики за сегодня: {row}")
        
        if row and row[0] is not None and row[0] > 0:
            return {
                'meal_count': row[0],
                'total_calories': round(row[1] or 0, 1),
                'total_protein': round(row[2] or 0, 1),
                'total_fat': round(row[3] or 0, 1),
                'total_carbs': round(row[4] or 0, 1)
            }
        
        # Если за сегодня нет данных, показываем за последние 24 часа
        cursor.execute('''
            SELECT 
                COUNT(*) as meal_count,
                SUM(calories) as total_calories,
                SUM(protein) as total_protein,
                SUM(fat) as total_fat,
                SUM(carbs) as total_carbs
            FROM meals 
            WHERE user_id = ? AND timestamp >= datetime('now', '-1 day')
        ''', (user_id,))
        
        row = cursor.fetchone()
        print(f"📊 Результат запроса статистики за 24 часа: {row}")
        
        if row and row[0] is not None:
            return {
                'meal_count': row[0],
                'total_calories': round(row[1] or 0, 1),
                'total_protein': round(row[2] or 0, 1),
                'total_fat': round(row[3] or 0, 1),
                'total_carbs': round(row[4] or 0, 1),
                'period': '24 часа'
            }
        
        return {
            'meal_count': 0,
            'total_calories': 0,
            'total_protein': 0,
            'total_fat': 0,
            'total_carbs': 0,
            'period': 'сегодня'
        }

    def get_period_stats(self, user_id, days=7):
        """Получает статистику за указанный период в днях"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT DATE(timestamp)) as days_count,
                COUNT(*) as meal_count,
                SUM(calories) as total_calories,
                SUM(protein) as total_protein,
                SUM(fat) as total_fat,
                SUM(carbs) as total_carbs,
                AVG(calories) as avg_daily_calories
            FROM meals 
            WHERE user_id = ? AND timestamp >= datetime('now', '-' || ? || ' days')
        ''', (user_id, days))
        
        row = cursor.fetchone()
        result = {
            'days_count': row[0] or 0,
            'meal_count': row[1] or 0,
            'total_calories': round(row[2] or 0, 1),
            'total_protein': round(row[3] or 0, 1),
            'total_fat': round(row[4] or 0, 1),
            'total_carbs': round(row[5] or 0, 1),
            'avg_daily_calories': round(row[6] or 0, 1) if row[0] else 0,
            'period': f'{days} дней'
        }
        
        # Самые частые продукты за период
        cursor.execute('''
            SELECT product, COUNT(*) as count, AVG(weight) as avg_weight
            FROM meals 
            WHERE user_id = ? AND timestamp >= datetime('now', '-' || ? || ' days')
            GROUP BY product 
            ORDER BY count DESC 
            LIMIT 5
        ''', (user_id, days))
        
        result['common_foods'] = []
        for row in cursor.fetchall():
            result['common_foods'].append((row[0], row[1], round(row[2], 1)))
        
        return result

    def get_monthly_stats(self, user_id, months=1):
        """Получает статистику за указанное количество месяцев"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT DATE(timestamp)) as days_count,
                COUNT(*) as meal_count,
                SUM(calories) as total_calories,
                SUM(protein) as total_protein,
                SUM(fat) as total_fat,
                SUM(carbs) as total_carbs,
                AVG(calories) as avg_daily_calories
            FROM meals 
            WHERE user_id = ? AND timestamp >= datetime('now', '-' || ? || ' months')
        ''', (user_id, months))
        
        row = cursor.fetchone()
        result = {
            'days_count': row[0] or 0,
            'meal_count': row[1] or 0,
            'total_calories': round(row[2] or 0, 1),
            'total_protein': round(row[3] or 0, 1),
            'total_fat': round(row[4] or 0, 1),
            'total_carbs': round(row[5] or 0, 1),
            'avg_daily_calories': round(row[6] or 0, 1) if row[0] else 0,
            'period': f'{months} месяц' if months == 1 else f'{months} месяцев'
        }
        
        return result

    def get_custom_period_stats(self, user_id, start_date, end_date):
        """Получает статистику за произвольный период"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(DISTINCT DATE(timestamp)) as days_count,
                COUNT(*) as meal_count,
                SUM(calories) as total_calories,
                SUM(protein) as total_protein,
                SUM(fat) as total_fat,
                SUM(carbs) as total_carbs,
                AVG(calories) as avg_daily_calories
            FROM meals 
            WHERE user_id = ? AND DATE(timestamp) BETWEEN ? AND ?
        ''', (user_id, start_date, end_date))
        
        row = cursor.fetchone()
        result = {
            'days_count': row[0] or 0,
            'meal_count': row[1] or 0,
            'total_calories': round(row[2] or 0, 1),
            'total_protein': round(row[3] or 0, 1),
            'total_fat': round(row[4] or 0, 1),
            'total_carbs': round(row[5] or 0, 1),
            'avg_daily_calories': round(row[6] or 0, 1) if row[0] else 0,
            'period': f'с {start_date} по {end_date}'
        }
        
        return result

    def add_feedback(self, user_id, feedback_text):
        """Добавляет отзыв в базу данных"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO feedback (user_id, feedback_text)
                VALUES (?, ?)
            ''', (user_id, feedback_text))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления отзыва: {e}")
            return False

    def get_recent_meals(self, user_id, limit=10):
        """Получает последние приемы пищи"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT product, weight, calories, protein, fat, carbs, timestamp 
            FROM meals 
            WHERE user_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        meals = []
        for row in cursor.fetchall():
            meals.append({
                'product': row[0],
                'weight': row[1],
                'calories': row[2],
                'protein': row[3],
                'fat': row[4],
                'carbs': row[5],
                'timestamp': row[6]
            })
        return meals

    def get_user_meals_today(self, user_id):
        """Получает все приемы пищи пользователя за сегодня"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT product, weight, calories, protein, fat, carbs, type
            FROM meals 
            WHERE user_id = ? AND DATE(timestamp) = CURRENT_DATE
            ORDER BY timestamp
        ''', (user_id,))
        
        meals = []
        for row in cursor.fetchall():
            meals.append({
                'product': row[0],
                'weight': row[1],
                'calories': row[2],
                'protein': row[3],
                'fat': row[4],
                'carbs': row[5],
                'type': row[6]
            })
        return meals

    def clear_user_data(self, user_id):
        """Очищает все данные пользователя (для тестирования)"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('DELETE FROM meals WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM user_profiles WHERE user_id = ?', (user_id,))
            cursor.execute('DELETE FROM feedback WHERE user_id = ?', (user_id,))
            self.conn.commit()
            print(f"✅ Данные пользователя {user_id} очищены")
            return True
        except Exception as e:
            print(f"❌ Ошибка очистки данных: {e}")
            return False