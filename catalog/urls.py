from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:slug>/", views.product_list_by_category, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
]