from django.contrib.auth import get_user_model
from django.db import models

from products.models import Variation
from products.views import MoneyMixin


class Order(models.Model, MoneyMixin):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE,
        related_name='orders'
    )
    total = models.FloatField()
    total_items = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=100, default='P',
        choices=(
            ('P', 'Pending'),
            ('A', 'Approved'),
            ('R', 'Rejected'),
            ('S', 'Shipped'),
            ('D', 'Delivered'),
            ('C', 'Cancelled'),
            ('F', 'Finished')
        )
    )

    def get_price(self):
        return self.to_money(self.total)

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model, MoneyMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Variation, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    image = models.CharField(max_length=1000, null=True, blank=True)

    def get_price(self):
        return self.to_money(self.price)

    def __str__(self) -> str:
        return f'Item {self.id} of order {self.order.id}'
