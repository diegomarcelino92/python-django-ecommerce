from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total',
        'status',
    )
    list_filter = (
        'user',
        'status',
    )
    search_fields = (
        'user',
        'status',
    )
