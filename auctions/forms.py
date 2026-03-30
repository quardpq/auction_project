from django import forms
from .models import Profile, Lot

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'address', 'bio']
        labels = {
            'full_name': 'Ваше полное имя (ФИО)',
            'phone': 'Номер телефона',
            'address': 'Адрес доставки',
            'bio': 'О себе',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-6 py-4 rounded-2xl border-2 border-gray-100 focus:border-blue-500 outline-none transition font-medium',
                'placeholder': 'Иванов Иван Иванович'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-6 py-4 rounded-2xl border-2 border-gray-100 focus:border-blue-500 outline-none transition font-medium',
                'placeholder': '+7 (999) 000-00-00'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'w-full px-6 py-4 rounded-2xl border-2 border-gray-100 focus:border-blue-500 outline-none transition font-medium',
                'placeholder': 'Город, улица, дом...'
            }),
            'bio': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'w-full px-6 py-4 rounded-2xl border-2 border-gray-100 focus:border-blue-500 outline-none transition font-medium',
                'placeholder': 'Расскажите немного о себе...'
            }),
        }

class LotForm(forms.ModelForm):
    class Meta:
        model = Lot
        # Убедись, что в модели поле называется current_price или starting_bid
        fields = ['title', 'description', 'current_price', 'image', 'category', 'end_date']
        labels = {
            'title': 'Название лота',
            'description': 'Описание товара',
            'current_price': 'Стартовая цена (₽)',
            'image': 'Изображение товара',
            'category': 'Категория',
            'end_date': 'Дата окончания торгов',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-blue-500 outline-none transition',
                'placeholder': 'Например: Сет колес Zeiss'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-blue-500 outline-none transition',
                'placeholder': 'Подробно опишите состояние и характеристики...'
            }),
            'current_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-blue-500 outline-none transition',
                'placeholder': '0.00'
            }),
            # ЗАМЕНА: Теперь это поле для выбора файла
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-blue-500 outline-none transition cursor-pointer file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-blue-500 outline-none transition cursor-pointer'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local', 
                'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-100 focus:border-blue-500 outline-none transition'
            }),
        }