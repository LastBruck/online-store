from django.urls import path
from .views import CartDetailView

urlpatterns = [
    path("basket", CartDetailView.as_view(), name="basket"),
]
