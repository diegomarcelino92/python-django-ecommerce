from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView

from products.models import Product


class ProductList(ListView):
    model = Product

    def get(self, request):
        return HttpResponse('List')


class ProductDetail(View):
    ...


class ProductCart(View):
    ...


class ProductCartAdd(View):
    ...


class ProductCartRemove(View):
    ...
