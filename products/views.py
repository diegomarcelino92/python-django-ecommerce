from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView

from products.models import Product


class ProductList(ListView):
    model = Product
    template_name = 'list.html'

    # def get(self, request):
    #     return HttpResponse('List')


class ProductDetail(View):
    ...


class ProductCart(View):
    ...


class ProductCartAdd(View):
    ...


class ProductCartRemove(View):
    ...
