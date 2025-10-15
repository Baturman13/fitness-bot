# recommendations.py
class RecommendationSystem:
    def __init__(self):
        pass
    
    def calculate_daily_needs(self, profile):
        """Рассчитывает суточные потребности на основе профиля"""
        if not all([profile.get('weight'), profile.get('height'), profile.get('age'), profile.get('gender')]):
            return None
        
        weight = profile['weight']
        height = profile['height']
        age = profile['age']
        gender = profile['gender']
        activity_level = profile.get('activity_level', 'moderate')
        goal = profile.get('goal', 'maintain')
        
        # Базальный метаболизм (формула Миффлина-Сан Жеора)
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Коэффициент активности
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        tdee = bmr * activity_multipliers.get(activity_level, 1.55)
        
        # Корректировка по цели
        goal_adjustments = {
            'lose': 0.85,
            'maintain': 1.0,
            'gain': 1.15
        }
        
        daily_calories = tdee * goal_adjustments.get(goal, 1.0)
        
        # Расчет БЖУ
        protein = weight * 2.2  # 2.2г белка на кг веса
        fat = (daily_calories * 0.25) / 9  # 25% от калорий, 9 ккал/г
        carbs = (daily_calories - (protein * 4 + fat * 9)) / 4  # остаток калорий, 4 ккал/г
        
        return {
            'daily_calories': round(daily_calories),
            'daily_protein': round(protein),
            'daily_fat': round(fat),
            'daily_carbs': round(carbs)
        }
    
    def generate_nutrition_recommendations(self, profile, analytics):
        """Генерирует рекомендации по питанию"""
        recommendations = []
        
        if not profile:
            return ["Заполните ваш профиль для персональных рекомендаций! Используйте /profile"]
        
        daily_needs = self.calculate_daily_needs(profile)
        if not daily_needs:
            return ["Недостаточно данных в профиле для расчетов"]
        
        avg_calories = analytics.get('avg_daily_calories', 0)
        target_calories = daily_needs['daily_calories']
        
        # Рекомендации по калориям
        if avg_calories < target_calories * 0.8:
            recommendations.append("📉 Вы потребляете слишком мало калорий. Увеличьте рацион для достижения цели.")
        elif avg_calories > target_calories * 1.2:
            recommendations.append("📈 Вы потребляете слишком много калорий. Скорректируйте питание для достижения цели.")
        else:
            recommendations.append("🎯 Отличный баланс калорий! Продолжайте в том же духе.")
        
        # Рекомендации по разнообразию
        common_foods_count = len(analytics.get('common_foods', []))
        if common_foods_count < 10:
            recommendations.append("🍎 Попробуйте разнообразить рацион. Добавьте больше фруктов и овощей.")
        
        # Рекомендации по цели
        goal = profile.get('goal')
        if goal == 'lose':
            recommendations.append("💧 Пейте больше воды перед едой - это поможет контролировать аппетит.")
            recommendations.append("🥗 Увеличьте потребление клетчатки - овощи, цельнозерновые продукты.")
        elif goal == 'gain':
            recommendations.append("💪 Увеличьте потребление белка для роста мышц.")
            recommendations.append("🥑 Добавьте полезные жиры: орехи, авокадо, оливковое масло.")
        
        return recommendations
    
    def generate_training_recommendations(self, profile):
        """Генерирует рекомендации по тренировкам"""
        if not profile:
            return ["Заполните профиль для получения персональных тренировочных рекомендаций!"]
        
        recommendations = []
        goal = profile.get('goal')
        activity_level = profile.get('activity_level')
        
        if goal == 'lose':
            recommendations.append("🏃‍♂️ Кардио тренировки: 3-5 раз в неделю по 30-45 минут")
            recommendations.append("💪 Силовые тренировки: 2-3 раза в неделю для сохранения мышц")
            recommendations.append("🚶‍♂️ Ежедневная активность: 10,000 шагов")
            
        elif goal == 'gain':
            recommendations.append("🏋️‍♂️ Силовые тренировки: 3-4 раза в неделю, фокус на прогрессию нагрузок")
            recommendations.append("🔋 Питание до/после тренировки: белки + углеводы")
            recommendations.append("💤 Восстановление: 7-9 часов сна, дни отдыха между тренировками")
            
        else:  # maintain
            recommendations.append("⚖️ Сбалансированные тренировки: 2-3 силовых + 2-3 кардио в неделю")
            recommendations.append("🎯 Функциональный тренинг: упражнения для повседневной активности")
            recommendations.append("🧘‍♂️ Не забывайте про растяжку и мобильность")
        
        # Рекомендации по уровню активности
        if activity_level in ['sedentary', 'light']:
            recommendations.append("📈 Начните с малого: 2-3 тренировки в неделю, постепенно увеличивайте нагрузку")
        
        return recommendations
    
    def get_progress_analysis(self, profile, analytics):
        """Анализ прогресса пользователя"""
        if not profile:
            return "Заполните профиль для анализа прогресса!"
        
        current_weight = profile.get('weight')
        target_weight = profile.get('target_weight')
        goal = profile.get('goal')
        
        if not current_weight or not target_weight:
            return "Укажите текущий и желаемый вес в профиле для анализа прогресса!"
        
        weight_difference = current_weight - target_weight
        
        if goal == 'lose':
            if weight_difference > 0:
                return f"🎯 До цели: {weight_difference:.1f}кг. Продолжайте двигаться в выбранном направлении!"
            else:
                return "🎉 Поздравляем! Вы достигли целевого веса!"
        elif goal == 'gain':
            if weight_difference < 0:
                return f"🎯 До цели: {abs(weight_difference):.1f}кг. Продолжайте набирать массу!"
            else:
                return "🎉 Поздравляем! Вы достигли целевого веса!"
        
        return "⚖️ Вы поддерживаете вес. Отличная работа!"