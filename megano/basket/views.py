from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from .cart import Cart


class CartDetailView(APIView):
    """APIView для корзины, реализация методов get, post и delete"""

    def get_cart_items(self, cart):
        cart_items = []
        for item in cart:
            product = Product.objects.get(id=item["product_id"])
            cart_item = {
                "id": product.id,
                "category": product.category.id,
                "price": float(item["price"]),
                "count": item["quantity"],
                "date": product.date.strftime("%a %b %d %Y %H:%M:%S GMT%z (%Z)"),
                "title": product.title,
                "description": product.description,
                "freeDelivery": product.freeDelivery,
                "images": [
                    {"src": image.image.url, "alt": image.alt()}
                    for image in product.images.all()
                ],
                "tags": [
                    {"id": tag.id, "name": tag.name} for tag in product.tags.all()
                ],
                "reviews": product.reviews_count(),
                "rating": product.average_rating(),
            }
            cart_items.append(cart_item)
        return cart_items

    def get(self, request):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def post(self, request):
        product_id = request.data.get("id")
        quantity = int(request.data.get("count", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.add(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)

    def delete(self, request):
        product_id = request.data.get("id")
        quantity = request.data.get("count", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        cart = Cart(request)
        cart.remove(product, quantity)
        cart_items = self.get_cart_items(cart)
        return Response(cart_items)
