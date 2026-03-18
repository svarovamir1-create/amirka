from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock", "is_active")
    search_fields = ("name",)
    list_filter = ("category", "is_active")
    inlines = [ProductImageInline]


admin.site.register(Category)