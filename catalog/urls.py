from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    # Главная
    path("", views.home, name="home"),

    # Каталог
    path("category/<slug:slug>/", views.product_list_by_category, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),

    # Корзина
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove"),
    path("cart/increase/<int:product_id>/", views.increase_quantity, name="increase"),
    path("cart/decrease/<int:product_id>/", views.decrease_quantity, name="decrease"),

    # 🔥 АККАУНТЫ
    path("register/", views.register, name="register"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
path("logout/", views.logout_view, name="logout"),
