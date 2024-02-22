from django.shortcuts import redirect, render
from django.views import View

from orders.models import Order, OrderItem
from products.models import Variation
from products.views import CartMixin


class OrderPay(View, CartMixin):
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

        _, cart_total_price = self.get_cart_calc(cart)
        self.request.session.save()

        order = Order(
            user=self.request.user,
            total=cart_total_price,
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
        return redirect('orders:list')


class OrderClose(View):
    pass


class OrderDetail(View):
    pass


class OrderList(View):
    def get(self, *args, **kwargs):
        return render(self.request, 'order_list.html')
