from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Lot, Bid, Category

# Регистрация кастомного пользователя
admin.site.register(User, UserAdmin)

# Регистрация профилей, чтобы видеть ФИО и телефоны
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone'] # Колонки, которые будут видны в списке
    search_fields = ['user__username', 'full_name', 'phone'] # Поиск по этим полям

# Регистрация остальных моделей (если еще не сделал)
admin.site.register(Lot)
admin.site.register(Bid)
admin.site.register(Category)