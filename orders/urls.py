from django.urls import path

from orders.views import OrderClose, OrderDetail, OrderList, OrderPay

app_name = 'orders'

urlpatterns = [
    path('', OrderPay.as_view(), name='pay'),
    path('close/', OrderClose.as_view(), name='close'),
    path('detail/', OrderDetail.as_view(), name='detail'),
    path('list/', OrderList.as_view(), name='list'),
]
