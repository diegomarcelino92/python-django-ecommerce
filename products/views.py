from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from products.models import Product, Variation


class ProductList(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 30


class ProductDetail(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_url_kwargs = 'slug'


class ProductCart(View):
    ...


class ProductCartAdd(View):
    def get(self, *args, **kwargs):
        referer = self.request.META.get('HTTP_REFERER', reverse('products:list'))

        variation = self.__get_variation()

        if not variation:
            return redirect(referer)

        in_stock = self.has_stock(variation)

        if in_stock:
            self.__add_to_cart(variation)

        return redirect(referer)

    def has_stock(self, variation: Variation, quantity=1):
        if variation.stock < quantity:
            messages.error(self.request, 'Estoque insuficiente.')
            return False
        return True

    def __add_to_cart(self, variation):
        var_id = str(variation.id)
        cart = self.__get_cart()
        variation = self.__get_variation()

        if var_id in cart:
            quantity = cart[var_id]['quantity'] + 1

            in_stock = self.has_stock(variation, quantity)

            if in_stock:
                cart[var_id]['quantity'] = quantity
                cart[var_id]['total'] = quantity * variation.price
                cart[var_id]['total_promo'] = quantity * variation.price_promo
            else:
                return
        else:
            cart[var_id] = {
                'quantity': 1,
                'price': variation.price,
                'total': variation.price,
                'price_promo': variation.price_promo,
                'total_promo': variation.price_promo,
                'name': variation.product.name,
                'variation': variation.name,
                'slug': variation.product.slug,
                'image': variation.product.image.url,
            }

        self.request.session.save()
        messages.success(self.request, 'Produto adicionado ao carrinho.')

    def __get_variation(self) -> Variation:
        var_id = self.request.GET.get('vid')

        if not var_id:
            messages.error(self.request, 'Produto não encontrado.')
            return None

        variation = Variation.objects.get(id=var_id)

        if not variation:
            messages.error(self.request, 'Produto não encontrado.')
            return None

        return variation

    def __get_cart(self):
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}

        return self.request.session.get('cart')


class ProductCartRemove(View):
    ...
