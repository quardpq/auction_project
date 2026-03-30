from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator

# Функция для расчета даты окончания (по умолчанию +7 дней)
def default_end_date():
    return timezone.now() + timedelta(days=7)

class User(AbstractUser):
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="auctions_user_set",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="auctions_user_permissions_set",
        blank=True,
    )

class Category(models.Model):
    name = models.CharField(max_length=64)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Lot(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название лота")
    description = models.TextField(verbose_name="Описание")
    current_price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name="Текущая цена")
    
    # ИЗМЕНЕНО: Теперь это поле для загрузки файлов
    image = models.ImageField(upload_to='lots/%Y/%m/%d/', blank=True, null=True, verbose_name="Изображение лота")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="lots", verbose_name="Категория")
    active = models.BooleanField(default=True, verbose_name="Активен")
    end_date = models.DateTimeField(default=default_end_date, verbose_name="Дата окончания торгов")

    @property
    def is_expired(self):
        return timezone.now() > self.end_date

    @property
    def winner(self):
        highest_bid = self.bids.order_by('-amount').first()
        return highest_bid.user if highest_bid else None

    @property
    def winning_bid(self):
        return self.bids.order_by('-amount').first()

    class Meta:
        verbose_name = "Лот"
        verbose_name_plural = "Лоты"

    def __str__(self):
        return self.title

class Bid(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="bids")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ставка"
        verbose_name_plural = "Ставки"

    def __str__(self):
        return f"{self.amount} ₽ на {self.lot.title}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, verbose_name="ФИО", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    address = models.TextField(verbose_name="Адрес доставки", blank=True)
    bio = models.TextField(verbose_name="О себе", blank=True)

    def __str__(self):
        return f"Профиль {self.user.username}"