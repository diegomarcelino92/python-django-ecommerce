from django.urls import path

from products.views import (ProductCart, ProductCartAdd, ProductCartRemove,
                            ProductDetail, ProductList)

app_name = 'products'

urlpatterns = [
    path('', ProductList.as_view(), name='list'),
    path('<slug>/', ProductDetail.as_view(), name='detail'),
    path('cart/', ProductCart.as_view(), name='cart'),
    path('cart/add/', ProductCartAdd.as_view(), name='cart-add'),
    path('cart/remove/', ProductCartRemove.as_view(), name='cart-remove'),
]
