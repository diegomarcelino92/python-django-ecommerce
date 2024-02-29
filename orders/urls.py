from django.urls import path

from orders.views import OrderCreate, OrderDetail, OrderList, OrderPay

app_name = 'orders'

urlpatterns = [
    path('', OrderCreate.as_view(), name='create'),
    path('pay/<int:order_id>/', OrderPay.as_view(), name='pay'),
    path('detail/<int:order_id>/', OrderDetail.as_view(), name='detail'),
    path('list/', OrderList.as_view(), name='list'),
]
