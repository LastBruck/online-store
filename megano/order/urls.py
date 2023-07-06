from django.urls import path
from .views import OrdersListView, OrderDetailView, PaymentView

urlpatterns = [
    path("orders", OrdersListView.as_view(), name="orders_list"),
    path("order/<int:pk>", OrderDetailView.as_view(), name="order_detail"),
    path("payment/<int:pk>", PaymentView.as_view(), name="payment"),
]
