from django.db import models

from user.models import Profile
from product.models import Product


class Order(models.Model):
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="orders")
    deliveryType = models.CharField(max_length=100, null=True, blank=True)
    paymentType = models.CharField(max_length=100, null=True, blank=True)
    totalCost = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    status = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    products = models.ManyToManyField(Product, related_name="orders")

    def fullName(self):
        return self.user.fullName

    def email(self):
        return self.user.email

    def phone(self):
        return self.user.phone

    def orderId(self):
        return {self.pk}

    def __str__(self):
        return f"Order: (pk={self.pk})"


class CountProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
