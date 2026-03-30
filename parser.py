import os
import django
import requests
from io import BytesIO
from django.core.files import File
from datetime import timedelta
from django.utils import timezone

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from auctions.models import Lot, Category, Bid

def run_clean_import():
    print("🧹 Полная очистка...")
    # Сначала удаляем ставки, потом лоты, чтобы не было конфликтов связей
    Bid.objects.all().delete()
    Lot.objects.all().delete()
    
    # Ссылки на фото для парсинга
    PHOTO_MAP = {
        "Solaris": "https://images.unsplash.com/photo-1590362891991-f776e747a588?q=80&w=800",
        "Camry": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?q=80&w=800",
        "Mercedes": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?q=80&w=800",
        "JCB": "https://images.unsplash.com/photo-1579412690850-ad4370caabb1?q=80&w=800",
        "Квартира": "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?q=80&w=800",
    }

    data = [
        {"t": "Hyundai Solaris, 2018 г.в.", "p": 920000, "cat": "Автомобили"},
        {"t": "Toyota Camry, 2014 г.в.", "p": 1550000, "cat": "Автомобили"},
        {"t": "Mercedes-Benz E-Class, 2015 г.в.", "p": 2300000, "cat": "Автомобили"},
        {"t": "Экскаватор JCB 3CX", "p": 4500000, "cat": "Спецтехника"},
        {"t": "Квартира, 54 м², г. Москва", "p": 12500000, "cat": "Недвижимость"},
    ]

    for item in data:
        title = item["t"]
        img_url = "https://via.placeholder.com/800"
        
        # Подбираем URL картинки по ключевому слову
        for key, url in PHOTO_MAP.items():
            if key.lower() in title.lower():
                img_url = url
                break
        
        category, _ = Category.objects.get_or_create(name=item["cat"])
        
        # Создаем объект лота (без картинки на первом этапе)
        # ИСПРАВЛЕНО: end_time заменено на end_date
        lot = Lot(
            title=title,
            description="Лот реализуется в рамках банкротства. Полный пакет документов.",
            current_price=item["p"],
            end_date=timezone.now() + timedelta(days=15),
            category=category,
            active=True
        )

        # СКАЧИВАЕМ И СОХРАНЯЕМ КАРТИНКУ
        try:
            response = requests.get(img_url, timeout=10)
            if response.status_code == 200:
                # Генерируем имя файла на основе заголовка или ID
                file_name = f"lot_{title[:10].replace(' ', '_')}.jpg"
                # Записываем контент в поле ImageField
                lot.image.save(file_name, File(BytesIO(response.content)), save=False)
        except Exception as e:
            print(f"⚠️ Ошибка загрузки фото для {title}: {e}")

        lot.save()
        print(f"✅ Добавлен лот и выгружено фото: {title}")

if __name__ == "__main__":
    run_clean_import()