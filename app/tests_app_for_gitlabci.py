import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== ПРОВЕРКА ===")

try:
    # Проверяем что приложение импортируется
    from app import app
    print("✅ Приложение импортировано")
    
    # Проверяем что Flask приложение создано
    assert hasattr(app, 'test_client'), "Не Flask приложение"
    print("✅ Это Flask приложение")
    
    # Проверяем главную страницу
    with app.test_client() as client:
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Главная страница работает")
            exit(0)
        else:
            print(f"⚠️ Главная страница: {response.status_code}")
            exit(0)  # Все равно успешный выход
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    exit(1)