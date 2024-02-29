from typing import Any

from django.contrib import messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, View

from orders.models import Order, OrderItem
from products.models import Variation
from products.views import CartMixin


class OrderCreate(View, CartMixin):
    def get(self, *args, **kwargs):
        cart = self.request.session.get('cart')

        if not self.request.user.is_authenticated:
            return redirect(self.request, 'profiles:create')

        if not cart:
            return redirect(self.request, 'products:list')

        cart_product_ids = [v for v in cart.keys() if v != 'total']

        products_variation = Variation.objects.select_related('product').filter(id__in=cart_product_ids)

        for var in products_variation:
            stock = var.stock
            var_id = str(var.id)
            quantity = cart[var_id]['quantity']

            if quantity > stock:
                cart[var_id]['quantity'] = stock

        _, cart_total_price, cart_total_itens = self.get_cart_calc(cart)
        self.request.session.save()

        order = Order(
            user=self.request.user,
            total=cart_total_price,
            total_items=cart_total_itens,
            status='Pending'
        )
        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=products_variation.filter(id=var['id']).first(),
                    price=var['price_promo'] if var['price_promo'] else var['price'],
                    quantity=var['quantity'],
                    image=var['image']
                ) for var in cart.values() if isinstance(var, dict)
            ]
        )

        del self.request.session['cart']
        self.request.session.save()
        messages.success(self.request, 'Pedido criado com sucesso')
        return redirect(reverse('orders:pay', kwargs={'order_id': order.pk}))


class OrderMixin(View):
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super().dispatch(self.request, *args, **kwargs)
        return redirect('profiles:create')

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class OrderPay(OrderMixin, DetailView):
    template_name = 'order_pay.html'
    model = Order
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'


class OrderDetail(OrderMixin, DetailView):
    template_name = 'order_detail.html'
    model = Order
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'


class OrderList(OrderMixin, ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
