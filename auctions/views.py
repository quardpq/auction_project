from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lot, Bid, Category, User, Profile
from .forms import ProfileForm, LotForm
from django.db import IntegrityError
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from django.http import JsonResponse

# --- ГЛАВНАЯ СТРАНИЦА ---
def index(request):
    lots_query = Lot.objects.filter(active=True).order_by('-id')
    
    q = request.GET.get('q')
    if q:
        lots_query = lots_query.filter(title__icontains=q) | lots_query.filter(description__icontains=q)
        
    cat_id = request.GET.get('category')
    if cat_id:
        lots_query = lots_query.filter(category_id=cat_id)

    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "lots": lots_query, 
        "categories": categories
    })

# --- ДЕТАЛИ ЛОТА ---
def lot_detail(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    return render(request, "auctions/lot_detail.html", {"lot": lot})

# --- СОЗДАНИЕ НОВОГО ЛОТА ---
@login_required
def create_lot(request):
    if request.method == "POST":
        form = LotForm(request.POST, request.FILES)
        if form.is_valid():
            new_lot = form.save(commit=False)
            new_lot.author = request.user 
            new_lot.save()
            return redirect('lot_detail', lot_id=new_lot.id)
    else:
        form = LotForm()
    return render(request, "auctions/create.html", {"form": form})

# --- СТАВКИ ---
@login_required
def place_bid(request, lot_id):
    lot = get_object_or_404(Lot, id=lot_id)
    if request.method == "POST":
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        
        if lot.is_expired:
            msg = "Торги завершены!"
            if is_ajax: return JsonResponse({"success": False, "error": msg}, status=400)
            messages.error(request, msg)
            return redirect('lot_detail', lot_id=lot.id)
            
        bid_value = request.POST.get("bid_amount")
        try:
            amount = Decimal(bid_value)
            if amount > lot.current_price:
                Bid.objects.create(user=request.user, lot=lot, amount=amount)
                lot.current_price = amount
                lot.save()
                
                if is_ajax:
                    return JsonResponse({
                        "success": True, 
                        "new_price": str(lot.current_price),
                        "message": f"Ставка {amount} ₽ принята!"
                    })
                messages.success(request, f"Ставка {amount} ₽ принята!")
            else:
                msg = f"Ставка должна быть выше {lot.current_price} ₽"
                if is_ajax: return JsonResponse({"success": False, "error": msg}, status=400)
                messages.error(request, msg)

        except (InvalidOperation, ValueError, TypeError):
            msg = "Некорректная сумма."
            if is_ajax: return JsonResponse({"success": False, "error": msg}, status=400)
            messages.error(request, msg)
            
    return redirect('lot_detail', lot_id=lot.id)

# --- ЛИЧНЫЙ КАБИНЕТ ---
@login_required
def profile_view(request):
    # Используем related_name='profile' как в твоем models.py
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные вашего профиля успешно сохранены!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
        
    return render(request, "auctions/profile.html", {"form": form})

@login_required
def my_bids(request):
    # Получаем все ставки пользователя
    user_bids = Bid.objects.filter(user=request.user).select_related('lot').order_by('-timestamp')
    return render(request, "auctions/my_bids.html", {"user_bids": user_bids})

# --- АВТОРИЗАЦИЯ ---
def login_view(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect("index")
        messages.error(request, "Логин или пароль неверны.")
    return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return redirect("index")

def register(request):
    if request.method == "POST":
        u = request.POST.get("username")
        e = request.POST.get("email")
        p = request.POST.get("password")
        c = request.POST.get("confirmation")

        # Проверка на пустые поля (защита от ValueError)
        if not u or not p:
            messages.error(request, "Имя пользователя и пароль обязательны.")
            return render(request, "auctions/register.html")

        if p != c:
            messages.error(request, "Пароли не совпадают.")
        else:
            try:
                user = User.objects.create_user(u, e, p)
                # Создаем профиль сразу, чтобы profile_view не тормозил
                Profile.objects.get_or_create(user=user)
                login(request, user)
                return redirect("index")
            except IntegrityError:
                messages.error(request, "Имя пользователя занято.")
    return render(request, "auctions/register.html")