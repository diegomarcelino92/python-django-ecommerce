from django.contrib import admin

from orders.models import Order, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'price',
        'quantity',
        'image',
    )
    list_filter = (
        'order',
        'product',
    )
    search_fields = (
        'order',
        'product',
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


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
    inlines = [OrderItemInline]
