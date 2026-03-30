import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from auctions.models import User

# Укажи здесь свои данные
username = 'quard'
email = 'quard@gmail.com'
password = 'quard182006'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Суперпользователь {username} создан!")
else:
    print(f"Пользователь {username} уже существует.")