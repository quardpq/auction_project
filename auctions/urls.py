from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lot/<int:lot_id>", views.lot_detail, name="lot_detail"),
    path("lot/<int:lot_id>/bid", views.place_bid, name="place_bid"),
    path("my-bids/", views.my_bids, name="my_bids"),
    # Блок авторизации
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("profile", views.profile_view, name="profile"),
    path("create", views.create_lot, name="create"),
]