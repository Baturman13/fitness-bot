# check_token.py
import requests

TOKEN = "8120512236:AAGCqMsgg1k6JY8FcpqxKvCfv5NXLhd7G4Q"
url = f"https://api.telegram.org/bot{TOKEN}/getMe"

print(f"🔐 Проверяем ПРАВИЛЬНЫЙ токен: {TOKEN}")
print(f"🌐 Отправляем запрос: {url}")

try:
    response = requests.get(url, timeout=10)
    print(f"📡 Статус ответа: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if data.get("ok"):
            bot_info = data["result"]
            print("✅ Токен верный! Информация о боте:")
            print(f"   Имя: {bot_info.get('first_name')}")
            print(f"   Username: @{bot_info.get('username')}")
            print(f"   ID: {bot_info.get('id')}")
        else:
            print("❌ Токен неверный или бот неактивен")
    else:
        print(f"❌ Ошибка HTTP: {response.status_code}")
        print(f"   Ответ: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Ошибка соединения: {e}")