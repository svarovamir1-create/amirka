from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product


def get_default_user():
    user = User.objects.first()
    return user.id if user else None


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=get_default_user
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ #{self.id} для {self.user.username if self.user else 'Без пользователя'}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"