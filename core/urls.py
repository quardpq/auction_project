from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # ПРАВИЛЬНЫЙ ИМПОРТ ЗДЕСЬ
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auctions.urls')), # Убедись, что название приложения совпадает
]

# Это позволит Django "видеть" твои загруженные картинки во время разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)