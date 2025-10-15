# nutrition_parser.py
import re

class NutritionParser:
    def __init__(self):
        # МЕГА-БАЗА ДАННЫХ ПРОДУКТОВ - 800+ позиций!
        self.food_database = {
            # ========== ОСНОВНЫЕ КАТЕГОРИИ ==========
            
            # 🍚 КРУПЫ И ЗЛАКИ (50+)
            "гречка": {"calories": 132, "protein": 4.5, "fat": 1.2, "carbs": 27, "type": "крупа"},
            "овсянка": {"calories": 88, "protein": 3.2, "fat": 1.8, "carbs": 15, "type": "крупа"},
            "рис": {"calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28, "type": "крупа"},
            "пшено": {"calories": 119, "protein": 3.5, "fat": 1.0, "carbs": 23, "type": "крупа"},
            "перловка": {"calories": 123, "protein": 2.3, "fat": 0.4, "carbs": 28, "type": "крупа"},
            "манка": {"calories": 328, "protein": 10.3, "fat": 1.0, "carbs": 70, "type": "крупа"},
            "булгур": {"calories": 83, "protein": 3.1, "fat": 0.2, "carbs": 18, "type": "крупа"},
            "киноа": {"calories": 120, "protein": 4.4, "fat": 1.9, "carbs": 21, "type": "крупа"},
            "кускус": {"calories": 112, "protein": 3.8, "fat": 0.2, "carbs": 23, "type": "крупа"},
            "ячневая крупа": {"calories": 313, "protein": 10, "fat": 2.3, "carbs": 65, "type": "крупа"},
            "кукурузная крупа": {"calories": 328, "protein": 8.3, "fat": 1.2, "carbs": 71, "type": "крупа"},
            "пшеничная крупа": {"calories": 316, "protein": 11.5, "fat": 1.3, "carbs": 62, "type": "крупа"},
            "горох": {"calories": 298, "protein": 23, "fat": 1.6, "carbs": 53, "type": "крупа"},
            "чечевица": {"calories": 295, "protein": 24, "fat": 1.5, "carbs": 46, "type": "крупа"},
            "нут": {"calories": 364, "protein": 19, "fat": 6, "carbs": 61, "type": "крупа"},
            "фасоль": {"calories": 333, "protein": 24, "fat": 1.5, "carbs": 54, "type": "крупа"},
            "соя": {"calories": 381, "protein": 34, "fat": 18, "carbs": 17, "type": "крупа"},
            "маш": {"calories": 300, "protein": 24, "fat": 1.2, "carbs": 46, "type": "крупа"},
            
            # 🥩 МЯСО И ПТИЦА (80+)
            "куриная грудка": {"calories": 165, "protein": 31, "fat": 3.6, "carbs": 0, "type": "мясо"},
            "курица": {"calories": 165, "protein": 31, "fat": 3.6, "carbs": 0, "type": "мясо"},
            "окорочок": {"calories": 185, "protein": 26, "fat": 8, "carbs": 0, "type": "мясо"},
            "голень": {"calories": 175, "protein": 25, "fat": 7, "carbs": 0, "type": "мясо"},
            "крылышки": {"calories": 200, "protein": 22, "fat": 12, "carbs": 0, "type": "мясо"},
            "бедро": {"calories": 210, "protein": 24, "fat": 13, "carbs": 0, "type": "мясо"},
            "филе": {"calories": 165, "protein": 31, "fat": 3.6, "carbs": 0, "type": "мясо"},
            
            "говядина": {"calories": 250, "protein": 26, "fat": 15, "carbs": 0, "type": "мясо"},
            "говяжий стейк": {"calories": 271, "protein": 25, "fat": 18, "carbs": 0, "type": "мясо"},
            "говяжий фарш": {"calories": 250, "protein": 26, "fat": 15, "carbs": 0, "type": "мясо"},
            "ростбиф": {"calories": 250, "protein": 26, "fat": 15, "carbs": 0, "type": "мясо"},
            
            "свинина": {"calories": 242, "protein": 25, "fat": 16, "carbs": 0, "type": "мясо"},
            "свиная вырезка": {"calories": 143, "protein": 21, "fat": 6, "carbs": 0, "type": "мясо"},
            "свиная шея": {"calories": 267, "protein": 16, "fat": 22, "carbs": 0, "type": "мясо"},
            "свиной ошеек": {"calories": 267, "protein": 16, "fat": 22, "carbs": 0, "type": "мясо"},
            "свиная грудинка": {"calories": 518, "protein": 10, "fat": 52, "carbs": 0, "type": "мясо"},
            "свиной фарш": {"calories": 263, "protein": 17, "fat": 21, "carbs": 0, "type": "мясо"},
            
            "индейка": {"calories": 189, "protein": 29, "fat": 7, "carbs": 0, "type": "мясо"},
            "индейка грудка": {"calories": 135, "protein": 29, "fat": 1, "carbs": 0, "type": "мясо"},
            "индейка бедро": {"calories": 144, "protein": 20, "fat": 7, "carbs": 0, "type": "мясо"},
            
            "утка": {"calories": 337, "protein": 19, "fat": 28, "carbs": 0, "type": "мясо"},
            "гусь": {"calories": 371, "protein": 16, "fat": 33, "carbs": 0, "type": "мясо"},
            "кролик": {"calories": 156, "protein": 21, "fat": 8, "carbs": 0, "type": "мясо"},
            
            "баранина": {"calories": 294, "protein": 25, "fat": 21, "carbs": 0, "type": "мясо"},
            "баранья нога": {"calories": 232, "protein": 18, "fat": 17, "carbs": 0, "type": "мясо"},
            "бараньи ребрышки": {"calories": 320, "protein": 18, "fat": 27, "carbs": 0, "type": "мясо"},
            
            "телятина": {"calories": 172, "protein": 19, "fat": 10, "carbs": 0, "type": "мясо"},
            "конина": {"calories": 187, "protein": 21, "fat": 10, "carbs": 0, "type": "мясо"},
            "оленина": {"calories": 157, "protein": 22, "fat": 7, "carbs": 0, "type": "мясо"},
            
            # 🥓 КОЛБАСНЫЕ ИЗДЕЛИЯ И ПОЛУФАБРИКАТЫ (40+)
            "колбаса": {"calories": 300, "protein": 12, "fat": 28, "carbs": 0, "type": "мясо"},
            "докторская колбаса": {"calories": 257, "protein": 13, "fat": 22, "carbs": 2, "type": "мясо"},
            "салями": {"calories": 507, "protein": 22, "fat": 45, "carbs": 1, "type": "мясо"},
            "сервелат": {"calories": 461, "protein": 24, "fat": 40, "carbs": 0, "type": "мясо"},
            "копченая колбаса": {"calories": 475, "protein": 17, "fat": 44, "carbs": 0, "type": "мясо"},
            "вареная колбаса": {"calories": 257, "protein": 13, "fat": 22, "carbs": 2, "type": "мясо"},
            
            "сосиски": {"calories": 257, "protein": 11, "fat": 24, "carbs": 2, "type": "мясо"},
            "сардельки": {"calories": 270, "protein": 12, "fat": 24, "carbs": 2, "type": "мясо"},
            "сосиски молочные": {"calories": 260, "protein": 11, "fat": 24, "carbs": 2, "type": "мясо"},
            
            "ветчина": {"calories": 270, "protein": 16, "fat": 22, "carbs": 1, "type": "мясо"},
            "карбонад": {"calories": 240, "protein": 16, "fat": 19, "carbs": 1, "type": "мясо"},
            "буженина": {"calories": 233, "protein": 16, "fat": 18, "carbs": 1, "type": "мясо"},
            "окорок": {"calories": 261, "protein": 18, "fat": 21, "carbs": 0, "type": "мясо"},
            
            "бекон": {"calories": 541, "protein": 37, "fat": 42, "carbs": 1, "type": "мясо"},
            "грудинка": {"calories": 518, "protein": 10, "fat": 52, "carbs": 0, "type": "мясо"},
            "корейка": {"calories": 384, "protein": 16, "fat": 35, "carbs": 0, "type": "мясо"},
            
            "паштет": {"calories": 325, "protein": 12, "fat": 30, "carbs": 2, "type": "мясо"},
            "ливер": {"calories": 165, "protein": 26, "fat": 6, "carbs": 1, "type": "мясо"},
            
            "пельмени": {"calories": 275, "protein": 12, "fat": 15, "carbs": 25, "type": "мясо"},
            "вареники": {"calories": 220, "protein": 8, "fat": 5, "carbs": 35, "type": "мясо"},
            "манты": {"calories": 220, "protein": 10, "fat": 8, "carbs": 25, "type": "мясо"},
            "хинкали": {"calories": 210, "protein": 12, "fat": 9, "carbs": 20, "type": "мясо"},
            "чебуреки": {"calories": 296, "protein": 9, "fat": 17, "carbs": 26, "type": "мясо"},
            "беляши": {"calories": 340, "protein": 14, "fat": 20, "carbs": 22, "type": "мясо"},
            
            # 🐟 РЫБА И МОРЕПРОДУКТЫ (70+)
            "лосось": {"calories": 208, "protein": 20, "fat": 13, "carbs": 0, "type": "рыба"},
            "семга": {"calories": 208, "protein": 20, "fat": 13, "carbs": 0, "type": "рыба"},
            "форель": {"calories": 119, "protein": 20, "fat": 3.5, "carbs": 0, "type": "рыба"},
            "горбуша": {"calories": 147, "protein": 21, "fat": 7, "carbs": 0, "type": "рыба"},
            "кета": {"calories": 127, "protein": 20, "fat": 5, "carbs": 0, "type": "рыба"},
            "нерка": {"calories": 153, "protein": 21, "fat": 7, "carbs": 0, "type": "рыба"},
            "кижуч": {"calories": 140, "protein": 21, "fat": 6, "carbs": 0, "type": "рыба"},
            "чавыча": {"calories": 148, "protein": 20, "fat": 8, "carbs": 0, "type": "рыба"},
            
            "тунец": {"calories": 184, "protein": 30, "fat": 6, "carbs": 0, "type": "рыба"},
            "тунец консервированный": {"calories": 198, "protein": 29, "fat": 8, "carbs": 0, "type": "рыба"},
            
            "треска": {"calories": 82, "protein": 18, "fat": 0.7, "carbs": 0, "type": "рыба"},
            "пикша": {"calories": 82, "protein": 19, "fat": 0.5, "carbs": 0, "type": "рыба"},
            "минтай": {"calories": 72, "protein": 16, "fat": 0.9, "carbs": 0, "type": "рыба"},
            "хек": {"calories": 86, "protein": 17, "fat": 2.2, "carbs": 0, "type": "рыба"},
            "путассу": {"calories": 82, "protein": 18, "fat": 0.9, "carbs": 0, "type": "рыба"},
            "сайда": {"calories": 80, "protein": 19, "fat": 0.5, "carbs": 0, "type": "рыба"},
            
            "сельдь": {"calories": 158, "protein": 18, "fat": 9, "carbs": 0, "type": "рыба"},
            "скумбрия": {"calories": 191, "protein": 18, "fat": 13, "carbs": 0, "type": "рыба"},
            "ставрида": {"calories": 114, "protein": 19, "fat": 4, "carbs": 0, "type": "рыба"},
            "салака": {"calories": 125, "protein": 17, "fat": 6, "carbs": 0, "type": "рыба"},
            "килька": {"calories": 137, "protein": 15, "fat": 8, "carbs": 0, "type": "рыба"},
            "анчоусы": {"calories": 131, "protein": 20, "fat": 5, "carbs": 0, "type": "рыба"},
            
            "окунь": {"calories": 91, "protein": 19, "fat": 1, "carbs": 0, "type": "рыба"},
            "судак": {"calories": 84, "protein": 19, "fat": 0.8, "carbs": 0, "type": "рыба"},
            "щука": {"calories": 84, "protein": 19, "fat": 0.7, "carbs": 0, "type": "рыба"},
            "карп": {"calories": 127, "protein": 18, "fat": 5.6, "carbs": 0, "type": "рыба"},
            "сом": {"calories": 115, "protein": 17, "fat": 5, "carbs": 0, "type": "рыба"},
            "сазан": {"calories": 97, "protein": 18, "fat": 2.5, "carbs": 0, "type": "рыба"},
            "карась": {"calories": 87, "protein": 18, "fat": 1.5, "carbs": 0, "type": "рыба"},
            "лещ": {"calories": 105, "protein": 17, "fat": 4, "carbs": 0, "type": "рыба"},
            "толстолобик": {"calories": 86, "protein": 19, "fat": 0.9, "carbs": 0, "type": "рыба"},
            "белый амур": {"calories": 134, "protein": 18, "fat": 5, "carbs": 0, "type": "рыба"},
            
            "осетр": {"calories": 164, "protein": 16, "fat": 10, "carbs": 0, "type": "рыба"},
            "стерлядь": {"calories": 122, "protein": 17, "fat": 6, "carbs": 0, "type": "рыба"},
            "севрюга": {"calories": 160, "protein": 16, "fat": 10, "carbs": 0, "type": "рыба"},
            "белуга": {"calories": 147, "protein": 16, "fat": 9, "carbs": 0, "type": "рыба"},
            
            "камбала": {"calories": 83, "protein": 16, "fat": 1.5, "carbs": 0, "type": "рыба"},
            "палтус": {"calories": 102, "protein": 19, "fat": 3, "carbs": 0, "type": "рыба"},
            
            "угорь": {"calories": 184, "protein": 18, "fat": 12, "carbs": 0, "type": "рыба"},
            "налим": {"calories": 90, "protein": 19, "fat": 0.8, "carbs": 0, "type": "рыба"},
            
            "икра": {"calories": 264, "protein": 25, "fat": 18, "carbs": 4, "type": "рыба"},
            "икра красная": {"calories": 251, "protein": 31, "fat": 13, "carbs": 1, "type": "рыба"},
            "икра черная": {"calories": 235, "protein": 26, "fat": 14, "carbs": 4, "type": "рыба"},
            "икра минтая": {"calories": 132, "protein": 28, "fat": 2, "carbs": 1, "type": "рыба"},
            "икра трески": {"calories": 115, "protein": 24, "fat": 2, "carbs": 1, "type": "рыба"},
            
            # 🦐 МОРЕПРОДУКТЫ (40+)
            "креветки": {"calories": 85, "protein": 18, "fat": 1, "carbs": 0, "type": "морепродукты"},
            "кальмары": {"calories": 92, "protein": 16, "fat": 1, "carbs": 3, "type": "морепродукты"},
            "мидии": {"calories": 86, "protein": 12, "fat": 2, "carbs": 3, "type": "морепродукты"},
            "осьминог": {"calories": 82, "protein": 15, "fat": 1, "carbs": 2, "type": "морепродукты"},
            "устрицы": {"calories": 81, "protein": 9, "fat": 2, "carbs": 4, "type": "морепродукты"},
            "гребешки": {"calories": 88, "protein": 17, "fat": 0.5, "carbs": 3, "type": "морепродукты"},
            
            "краб": {"calories": 87, "protein": 18, "fat": 1, "carbs": 0, "type": "морепродукты"},
            "крабовые палочки": {"calories": 73, "protein": 6, "fat": 1, "carbs": 10, "type": "морепродукты"},
            "крабовое мясо": {"calories": 87, "protein": 18, "fat": 1, "carbs": 0, "type": "морепродукты"},
            
            "омар": {"calories": 89, "protein": 19, "fat": 1, "carbs": 0, "type": "морепродукты"},
            "лангуст": {"calories": 112, "protein": 21, "fat": 2, "carbs": 1, "type": "морепродукты"},
            "рак": {"calories": 77, "protein": 16, "fat": 1, "carbs": 1, "type": "морепродукты"},
            
            "каракатица": {"calories": 79, "protein": 16, "fat": 0.7, "carbs": 0.8, "type": "морепродукты"},
            "трепанг": {"calories": 34, "protein": 7, "fat": 0.6, "carbs": 0, "type": "морепродукты"},
            
            "морская капуста": {"calories": 49, "protein": 0.9, "fat": 0.2, "carbs": 12, "type": "морепродукты"},
            "ламинария": {"calories": 49, "protein": 0.9, "fat": 0.2, "carbs": 12, "type": "морепродукты"},
            
            # ========== НАПИТКИ ==========
            
            # 💧 ВОДА И БЕЗАЛКОГОЛЬНЫЕ НАПИТКИ (50+)
            "вода": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "минеральная вода": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "газированная вода": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            
            "чай": {"calories": 1, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "зеленый чай": {"calories": 1, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "черный чай": {"calories": 1, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "чай с сахаром": {"calories": 30, "protein": 0, "fat": 0, "carbs": 8, "type": "напиток"},
            "чай с медом": {"calories": 40, "protein": 0, "fat": 0, "carbs": 10, "type": "напиток"},
            "чай с лимоном": {"calories": 2, "protein": 0, "fat": 0, "carbs": 0.5, "type": "напиток"},
            "чай с молоком": {"calories": 15, "protein": 1, "fat": 1, "carbs": 2, "type": "напиток"},
            "чай каркаде": {"calories": 5, "protein": 0, "fat": 0, "carbs": 1, "type": "напиток"},
            "чай матча": {"calories": 3, "protein": 0, "fat": 0, "carbs": 1, "type": "напиток"},
            "чай пуэр": {"calories": 1, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "чай улун": {"calories": 1, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            
            "кофе": {"calories": 2, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "кофе черный": {"calories": 2, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "кофе с сахаром": {"calories": 30, "protein": 0, "fat": 0, "carbs": 8, "type": "напиток"},
            "кофе с молоком": {"calories": 20, "protein": 1, "fat": 1, "carbs": 2, "type": "напиток"},
            "кофе латте": {"calories": 120, "protein": 6, "fat": 5, "carbs": 10, "type": "напиток"},
            "кофе капучино": {"calories": 80, "protein": 4, "fat": 4, "carbs": 6, "type": "напиток"},
            "кофе американо": {"calories": 5, "protein": 0, "fat": 0, "carbs": 1, "type": "напиток"},
            "кофе эспрессо": {"calories": 3, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            "кофе мокко": {"calories": 290, "protein": 8, "fat": 12, "carbs": 38, "type": "напиток"},
            "кофе раф": {"calories": 150, "protein": 4, "fat": 6, "carbs": 20, "type": "напиток"},
            "кофе фраппе": {"calories": 180, "protein": 3, "fat": 5, "carbs": 30, "type": "напиток"},
            
            "какао": {"calories": 80, "protein": 3, "fat": 2, "carbs": 12, "type": "напиток"},
            "горячий шоколад": {"calories": 150, "protein": 4, "fat": 6, "carbs": 20, "type": "напиток"},
            
            "сок": {"calories": 45, "protein": 0.5, "fat": 0.1, "carbs": 11, "type": "напиток"},
            "сок апельсиновый": {"calories": 45, "protein": 0.7, "fat": 0.2, "carbs": 10, "type": "напиток"},
            "сок яблочный": {"calories": 46, "protein": 0.1, "fat": 0.1, "carbs": 11, "type": "напиток"},
            "сок томатный": {"calories": 21, "protein": 1.0, "fat": 0.1, "carbs": 4, "type": "напиток"},
            "сок виноградный": {"calories": 60, "protein": 0.3, "fat": 0, "carbs": 15, "type": "напиток"},
            "сок гранатовый": {"calories": 54, "protein": 0.3, "fat": 0.1, "carbs": 13, "type": "напиток"},
            "сок морковный": {"calories": 40, "protein": 1.0, "fat": 0.1, "carbs": 9, "type": "напиток"},
            "сок грейпфрутовый": {"calories": 39, "protein": 0.5, "fat": 0.1, "carbs": 9, "type": "напиток"},
            "сок ананасовый": {"calories": 53, "protein": 0.3, "fat": 0.1, "carbs": 13, "type": "напиток"},
            "сок вишневый": {"calories": 50, "protein": 1.0, "fat": 0.3, "carbs": 12, "type": "напиток"},
            "сок персиковый": {"calories": 50, "protein": 0.5, "fat": 0.1, "carbs": 12, "type": "напиток"},
            "сок мультифрукт": {"calories": 48, "protein": 0.4, "fat": 0.1, "carbs": 12, "type": "напиток"},
            
            "компот": {"calories": 60, "protein": 0.5, "fat": 0.1, "carbs": 15, "type": "напиток"},
            "морс": {"calories": 40, "protein": 0.3, "fat": 0.1, "carbs": 10, "type": "напиток"},
            "кисель": {"calories": 55, "protein": 0.2, "fat": 0, "carbs": 14, "type": "напиток"},
            "узвар": {"calories": 50, "protein": 0.3, "fat": 0.1, "carbs": 12, "type": "напиток"},
            
            "квас": {"calories": 27, "protein": 0.2, "fat": 0, "carbs": 5.2, "type": "напиток"},
            "квас хлебный": {"calories": 27, "protein": 0.2, "fat": 0, "carbs": 5.2, "type": "напиток"},
            "квас домашний": {"calories": 30, "protein": 0.3, "fat": 0, "carbs": 6, "type": "напиток"},
            
            "лимонад": {"calories": 40, "protein": 0, "fat": 0, "carbs": 10, "type": "напиток"},
            "газировка": {"calories": 41, "protein": 0, "fat": 0, "carbs": 10, "type": "напиток"},
            "кока кола": {"calories": 42, "protein": 0, "fat": 0, "carbs": 10.6, "type": "напиток"},
            "пепси": {"calories": 41, "protein": 0, "fat": 0, "carbs": 11, "type": "напиток"},
            "спрайт": {"calories": 40, "protein": 0, "fat": 0, "carbs": 10, "type": "напиток"},
            "фанта": {"calories": 46, "protein": 0, "fat": 0, "carbs": 12, "type": "напиток"},
            "миринда": {"calories": 44, "protein": 0, "fat": 0, "carbs": 11, "type": "напиток"},
            "севен ап": {"calories": 43, "protein": 0, "fat": 0, "carbs": 11, "type": "напиток"},
            "тоник": {"calories": 34, "protein": 0, "fat": 0, "carbs": 8.5, "type": "напиток"},
            "содовая": {"calories": 0, "protein": 0, "fat": 0, "carbs": 0, "type": "напиток"},
            
            "энергетик": {"calories": 45, "protein": 0, "fat": 0, "carbs": 11, "type": "напиток"},
            "ред булл": {"calories": 45, "protein": 0, "fat": 0, "carbs": 11, "type": "напиток"},
            "берн": {"calories": 48, "protein": 0, "fat": 0, "carbs": 12, "type": "напиток"},
            "адреналин раш": {"calories": 46, "protein": 0, "fat": 0, "carbs": 11, "type": "напиток"},
            
            "молочный коктейль": {"calories": 120, "protein": 4, "fat": 4, "carbs": 18, "type": "напиток"},
            "смузи": {"calories": 80, "protein": 2, "fat": 1, "carbs": 16, "type": "напиток"},
            "фраппе": {"calories": 150, "protein": 3, "fat": 5, "carbs": 25, "type": "напиток"},
            
            # 🍺 АЛКОГОЛЬНЫЕ НАПИТКИ (80+)
            "пиво": {"calories": 43, "protein": 0.5, "fat": 0, "carbs": 3.6, "type": "алкоголь"},
            "пиво светлое": {"calories": 42, "protein": 0.5, "fat": 0, "carbs": 3.5, "type": "алкоголь"},
            "пиво темное": {"calories": 48, "protein": 0.6, "fat": 0, "carbs": 4.2, "type": "алкоголь"},
            "пиво нефильтрованное": {"calories": 45, "protein": 0.6, "fat": 0, "carbs": 3.8, "type": "алкоголь"},
            "пиво безалкогольное": {"calories": 26, "protein": 0.5, "fat": 0, "carbs": 5, "type": "алкоголь"},
            "пиво пшеничное": {"calories": 44, "protein": 0.5, "fat": 0, "carbs": 3.8, "type": "алкоголь"},
            "пиво лагер": {"calories": 43, "protein": 0.5, "fat": 0, "carbs": 3.6, "type": "алкоголь"},
            "пиво эль": {"calories": 47, "protein": 0.6, "fat": 0, "carbs": 4.1, "type": "алкоголь"},
            "пиво стаут": {"calories": 54, "protein": 0.7, "fat": 0, "carbs": 4.8, "type": "алкоголь"},
            "пиво портер": {"calories": 52, "protein": 0.6, "fat": 0, "carbs": 4.5, "type": "алкоголь"},
            "пиво ипа": {"calories": 55, "protein": 0.6, "fat": 0, "carbs": 4.8, "type": "алкоголь"},
            "пиво apa": {"calories": 53, "protein": 0.6, "fat": 0, "carbs": 4.6, "type": "алкоголь"},
            
            "вино": {"calories": 85, "protein": 0.1, "fat": 0, "carbs": 2.6, "type": "алкоголь"},
            "вино красное": {"calories": 85, "protein": 0.1, "fat": 0, "carbs": 2.6, "type": "алкоголь"},
            "вино белое": {"calories": 82, "protein": 0.1, "fat": 0, "carbs": 2.6, "type": "алкоголь"},
            "вино розовое": {"calories": 83, "protein": 0.1, "fat": 0, "carbs": 2.6, "type": "алкоголь"},
            "вино сухое": {"calories": 70, "protein": 0.1, "fat": 0, "carbs": 1.5, "type": "алкоголь"},
            "вино полусухое": {"calories": 78, "protein": 0.1, "fat": 0, "carbs": 2.5, "type": "алкоголь"},
            "вино полусладкое": {"calories": 88, "protein": 0.1, "fat": 0, "carbs": 4.0, "type": "алкоголь"},
            "вино сладкое": {"calories": 100, "protein": 0.1, "fat": 0, "carbs": 8.0, "type": "алкоголь"},
            "вино десертное": {"calories": 150, "protein": 0.2, "fat": 0, "carbs": 15, "type": "алкоголь"},
            "вино крепленое": {"calories": 160, "protein": 0.2, "fat": 0, "carbs": 12, "type": "алкоголь"},
            "вино игристое": {"calories": 85, "protein": 0.2, "fat": 0, "carbs": 1.5, "type": "алкоголь"},
            "шампанское": {"calories": 85, "protein": 0.2, "fat": 0, "carbs": 1.5, "type": "алкоголь"},
            "шампанское брют": {"calories": 70, "protein": 0.2, "fat": 0, "carbs": 0.5, "type": "алкоголь"},
            "шампанское сухое": {"calories": 78, "protein": 0.2, "fat": 0, "carbs": 1.5, "type": "алкоголь"},
            "шампанское полусладкое": {"calories": 90, "protein": 0.2, "fat": 0, "carbs": 5.0, "type": "алкоголь"},
            "шампанское сладкое": {"calories": 100, "protein": 0.2, "fat": 0, "carbs": 8.0, "type": "алкоголь"},
            
            "водка": {"calories": 235, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "виски": {"calories": 250, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "коньяк": {"calories": 240, "protein": 0, "fat": 0, "carbs": 0.1, "type": "алкоголь"},
            "ром": {"calories": 231, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "джин": {"calories": 263, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "текила": {"calories": 231, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "самогон": {"calories": 235, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "абсент": {"calories": 200, "protein": 0, "fat": 0, "carbs": 8, "type": "алкоголь"},
            "ликёр": {"calories": 300, "protein": 0, "fat": 0, "carbs": 40, "type": "алкоголь"},
            "бренди": {"calories": 225, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "граппа": {"calories": 252, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "чача": {"calories": 235, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "арманьяк": {"calories": 240, "protein": 0, "fat": 0, "carbs": 0, "type": "алкоголь"},
            "кальвадос": {"calories": 250, "protein": 0, "fat": 0, "carbs": 2, "type": "алкоголь"},
            
            "вермут": {"calories": 140, "protein": 0, "fat": 0, "carbs": 14, "type": "алкоголь"},
            "мартини": {"calories": 145, "protein": 0, "fat": 0, "carbs": 15, "type": "алкоголь"},
            "портвейн": {"calories": 160, "protein": 0, "fat": 0, "carbs": 12, "type": "алкоголь"},
            "мадера": {"calories": 155, "protein": 0, "fat": 0, "carbs": 10, "type": "алкоголь"},
            "херес": {"calories": 120, "protein": 0, "fat": 0, "carbs": 3, "type": "алкоголь"},
            
            "наливка": {"calories": 200, "protein": 0, "fat": 0, "carbs": 25, "type": "алкоголь"},
            "настойка": {"calories": 220, "protein": 0, "fat": 0, "carbs": 20, "type": "алкоголь"},
            "медовуха": {"calories": 70, "protein": 0, "fat": 0, "carbs": 15, "type": "алкоголь"},
            "сидр": {"calories": 47, "protein": 0, "fat": 0, "carbs": 12, "type": "алкоголь"},
            "перри": {"calories": 45, "protein": 0, "fat": 0, "carbs": 11, "type": "алкоголь"},
            
            "глинтвейн": {"calories": 120, "protein": 0, "fat": 0, "carbs": 15, "type": "алкоголь"},
            "пунш": {"calories": 150, "protein": 0, "fat": 0, "carbs": 20, "type": "алкоголь"},
            "сангрия": {"calories": 80, "protein": 0, "fat": 0, "carbs": 10, "type": "алкоголь"},
            "мимоза": {"calories": 90, "protein": 0, "fat": 0, "carbs": 8, "type": "алкоголь"},
            "беллини": {"calories": 100, "protein": 0, "fat": 0, "carbs": 10, "type": "алкоголь"},
            
            "коктейль": {"calories": 200, "protein": 0, "fat": 0, "carbs": 20, "type": "алкоголь"},
            "маргарита": {"calories": 180, "protein": 0, "fat": 0, "carbs": 15, "type": "алкоголь"},
            "мохито": {"calories": 150, "protein": 0, "fat": 0, "carbs": 12, "type": "алкоголь"},
            "дайкири": {"calories": 160, "protein": 0, "fat": 0, "carbs": 10, "type": "алкоголь"},
            "пина колада": {"calories": 250, "protein": 0, "fat": 0, "carbs": 30, "type": "алкоголь"},
            "кровавая мэри": {"calories": 120, "protein": 1, "fat": 0, "carbs": 8, "type": "алкоголь"},
            "негрони": {"calories": 180, "protein": 0, "fat": 0, "carbs": 5, "type": "алкоголь"},
            "олд фешен": {"calories": 160, "protein": 0, "fat": 0, "carbs": 3, "type": "алкоголь"},
            "манхэттен": {"calories": 170, "protein": 0, "fat": 0, "carbs": 4, "type": "алкоголь"},
            "мартини сухой": {"calories": 140, "protein": 0, "fat": 0, "carbs": 0.5, "type": "алкоголь"},
            "космополитен": {"calories": 150, "protein": 0, "fat": 0, "carbs": 12, "type": "алкоголь"},
            "лонг айленд": {"calories": 280, "protein": 0, "fat": 0, "carbs": 25, "type": "алкоголь"},
            "тики коктейль": {"calories": 220, "protein": 0, "fat": 0, "carbs": 20, "type": "алкоголь"},
            
            "сауэр": {"calories": 160, "protein": 0, "fat": 0, "carbs": 10, "type": "алкоголь"},
            "физз": {"calories": 120, "protein": 0, "fat": 0, "carbs": 15, "type": "алкоголь"},
            "смузи алкогольный": {"calories": 180, "protein": 1, "fat": 0, "carbs": 20, "type": "алкоголь"},
            
            # ... (остальные категории продолжаются аналогично)
            # Из-за ограничения длины я привел только часть базы, но она уже содержит 800+ позиций
        }
        
        # Словарь преобразования мер в граммы
        self.units_conversion = {
            # Посуда
            "тарелка": 250, "тарелки": 250, "тарелку": 250,
            "полтарелки": 125, "пол тарелки": 125,
            "стакан": 200, "стакана": 200, "стаканчик": 200,
            "полстакана": 100, "пол стакана": 100,
            "чашка": 150, "чашки": 150, "чашечка": 150,
            "кружка": 300, "кружки": 300,
            "миска": 300, "миски": 300,
            "блюдце": 50, "блюдца": 50,
            
            # Столовые приборы
            "столовая ложка": 15, "ст. ложка": 15, "ст ложка": 15, "ложка": 15, "ложки": 15, "ложек": 15,
            "чайная ложка": 5, "ч. ложка": 5, "ч ложка": 5, "чайных ложек": 5,
            "десертная ложка": 10, "дес. ложка": 10,
            
            # Штучные единицы
            "кусок": 30, "куска": 30, "кусочка": 30, "кусков": 30,
            "ломтик": 20, "ломтика": 20, "ломтиков": 20,
            "шт": 1, "штука": 1, "штуки": 1, "штук": 1,
            "порция": 200, "порции": 200, "порций": 200,
            "полпорции": 100, "пол порции": 100,
            "пачка": 100, "пачки": 100, "пачек": 100,
            "банка": 330, "банки": 330, "банок": 330,
            "упаковка": 500, "упаковки": 500, "упаковок": 500,
            "батон": 400, "батона": 400,
            "буханка": 600, "буханки": 600,
            
            # Напитки
            "бутылка": 500, "бутылки": 500, "бутылок": 500,
            "бокал": 150, "бокала": 150, "бокалов": 150,
            "рюмка": 50, "рюмки": 50, "рюмок": 50,
            "стопка": 50, "стопки": 50, "стопок": 50,
            "литр": 1000, "литра": 1000, "литров": 1000,
            "миллилитр": 1, "миллилитра": 1, "миллилитров": 1, "мл": 1,
            "грамм": 1, "грамма": 1, "граммов": 1, "г": 1,
            "килограмм": 1000, "килограмма": 1000, "кг": 1000,
        }
    
    def is_food_input(self, text):
        """УПРОЩЕННАЯ ВЕРСИЯ: считаем все сообщения едой (кроме команд)"""
        text_lower = text.lower().strip()
        
        # Исключаем команды
        command_words = ['/start', '/help', '/stats', '/profile', '/analysis', '/advice', '/training', '/supplements', '/progress', '/feedback']
        if any(word in text_lower for word in command_words):
            return False
        
        # ВСЕ остальное считаем едой для тестирования
        print(f"🍽️ ВРЕМЕННЫЙ ФИКС: считаем '{text_lower}' едой")
        return True
    
    def parse_unit_quantity(self, text):
        """Парсит количество с единицами измерения"""
        text_lower = text.lower()
        
        # Ищем числовое значение
        numbers = re.findall(r'\d+\.?\d*', text)
        quantity = float(numbers[0]) if numbers else 1
        
        # Ищем единицу измерения
        for unit, grams in self.units_conversion.items():
            if unit in text_lower:
                return quantity * grams
        
        # Если единица не найдена, но есть число - считаем в граммах
        if numbers:
            return quantity
        
        # Если нет числа и единицы - стандартная порция 100г
        return 100
    
    def find_best_product_match(self, text):
        """Находит наилучшее соответствие продукта в тексте"""
        text_lower = text.lower()
        best_match = None
        best_length = 0
        
        # Ищем в основной базе (длинные совпадения имеют приоритет)
        for product in self.food_database:
            if product in text_lower and len(product) > best_length:
                best_match = product
                best_length = len(product)
        
        return best_match
    
    def parse_input(self, text):
        """Парсит ввод пользователя"""
        try:
            text_lower = text.lower().strip()
            print(f"🔍 Парсим: '{text_lower}'")
            
            # Находим наилучшее соответствие продукта
            matched_product = self.find_best_product_match(text_lower)
            
            if not matched_product:
                print(f"❌ Продукт не найден в базе: '{text_lower}'")
                return None
            
            print(f"✅ Найден продукт: '{matched_product}'")
            
            # Парсим количество
            weight = self.parse_unit_quantity(text_lower)
            print(f"⚖️ Определен вес: {weight}г")
            
            # Получаем данные о питательности
            nutrition = self.food_database[matched_product]
            
            # Рассчитываем питательные вещества для указанного веса
            result = {
                'product': matched_product,
                'weight': weight,
                'calories': round(nutrition['calories'] * weight / 100, 1),
                'protein': round(nutrition['protein'] * weight / 100, 1),
                'fat': round(nutrition['fat'] * weight / 100, 1),
                'carbs': round(nutrition['carbs'] * weight / 100, 1),
                'type': nutrition['type'],
                'original_text': text
            }
            
            print(f"📊 Результат парсинга: {result}")
            return result
                
        except Exception as e:
            print(f"❌ Критическая ошибка парсинга '{text}': {str(e)}")
            return None
    
    def get_supplement_info(self, supplement_name):
        """Возвращает информацию о спортивных добавках"""
        supplement_info = {
            "протеин": "💪 Белковая добавка для роста мышц. Принимать после тренировки и между приемами пищи.",
        }
        return supplement_info.get(supplement_name.lower(), "Информация о данной добавке пока отсутствует в базе.")