from django.views import View
from django.views.generic.list import ListView

from products.models import Product


class ProductList(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 1


class ProductDetail(View):
    ...


class ProductCart(View):
    ...


class ProductCartAdd(View):
    ...


class ProductCartRemove(View):
    ...
