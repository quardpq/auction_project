import os
from pathlib import Path
import dj_database_url

# Определение базовой папки проекта
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-your-key-here'

# На сервере лучше держать False, но для отладки оставим True
DEBUG = True

# Разрешаем Render запускать ваш сайт
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auctions', 
    'django.contrib.humanize'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise помогает Django отдавать статические файлы на Render
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# --- НАСТРОЙКА БАЗЫ ДАННЫХ (ИСПРАВЛЕНО) ---
# По умолчанию используем SQLite (для твоего компьютера)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Если на Render задана переменная DATABASE_URL, переключаемся на Postgres
db_from_env = dj_database_url.config(conn_max_age=600)
if db_from_env:
    DATABASES['default'] = db_from_env

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Модель пользователя
AUTH_USER_MODEL = 'auctions.User'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'

# --- НАСТРОЙКИ СТАТИКИ ---
STATIC_URL = '/static/'
# Папка, куда Render соберет файлы
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Дополнительные места поиска статики
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Настройки медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Перезапуск деплоя