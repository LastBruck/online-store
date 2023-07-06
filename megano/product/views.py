from django.db.models import Count
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from .models import Product, Tag, Sale, Review, Category
from .serializers import (
    ProductSerializer,
    TagsProductSerializer,
    SaleSerializer,
    ReviewSerializer,
    CategorySerializer,
)


class CategoriesList(APIView):
    def get(self, request: Request):
        categories = Category.objects.filter(parent=None)
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)


class ProductDetail(APIView):
    def get(self, request: Request, pk):
        product = Product.objects.get(pk=pk)
        serialized = ProductSerializer(product, many=False)
        return Response(serialized.data)


class SalesList(APIView):
    def get(self, request: Request):
        sales = Sale.objects.all()
        serialized = SaleSerializer(sales, many=True)
        return Response({"items": serialized.data})


class LimitedList(APIView):
    def get(self, request: Request):
        products = Product.objects.filter(limited_edition=True)
        serialized = ProductSerializer(products, many=True)
        return Response(serialized.data)


class PopularList(APIView):
    def get(self, request: Request):
        products = (
            Product.objects.filter(active=True)
            .annotate(count_reviews=Count("reviews"))
            .order_by("-count_reviews")[:8]
        )
        serialized = ProductSerializer(products, many=True)
        return Response(serialized.data)


class CreateReview(CreateModelMixin, GenericAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk):
        product = Product.objects.get(id=pk)
        request.data["date"] = datetime.now()
        request.data["product"] = product.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Review.objects.create(
            author=request.data["author"],
            email=request.data["email"],
            text=request.data["text"],
            rate=request.data["rate"],
            date=datetime.now(),
            product_id=product.pk,
        )

        reviews = Review.objects.filter(product_id=product.pk)
        summa = sum([obj.rate for obj in reviews])
        product.rating = summa / len(reviews)
        product.save()
        return Response(request.data)


class TagsList(APIView):
    def get(self, request: Request):
        tags = Tag.objects.all()
        data = TagsProductSerializer(tags, many=True)
        return Response(data.data)


class BannersList(APIView):
    def get(self, request: Request):
        favourite_categories = [
            obj.pk for obj in Category.objects.filter(favourite=True)
        ]
        banners = Product.objects.filter(category_id__in=favourite_categories)
        serialized = ProductSerializer(banners, many=True)
        return Response(serialized.data)


def sort_products(request: Request, products):
    sort = request.GET.get("sort")
    sortType = request.GET.get("sortType")
    if sortType == "inc":
        sortType = "-"
    else:
        sortType = ""

    if sort == "reviews":
        products = (
            products.filter(active=True)
            .annotate(count_reviews=Count("reviews"))
            .order_by(f"{sortType}count_reviews")
            .prefetch_related("images", "reviews")
        )
    else:
        products = (
            products.filter(active=True)
            .order_by(f"{sortType}{sort}")
            .prefetch_related("images", "reviews")
        )
    return products


def filter_catalog(request: Request):
    name = request.query_params.get("filter[name]")
    min_price = request.query_params.get("filter[minPrice]")
    max_price = request.query_params.get("filter[maxPrice]")
    freeDelivery = request.query_params.get("filter[freeDelivery]")
    available = request.query_params.get("filter[available]")

    tags = request.query_params.getlist("tags[]")
    category = request.META["HTTP_REFERER"].split("/")[4]

    catalog = Product.objects
    if category:
        try:
            categories = [obj.pk for obj in Category.objects.filter(parent_id=category)]
            categories.append(int(category))
            catalog = catalog.filter(category_id__in=categories)
        except:
            if str(category).startswith("?filter="):
                if not name:
                    name = str(category).split("=")[1]
            else:
                category = ""

    if available == "true":
        if freeDelivery == "true":
            if tags:
                catalog = (
                    catalog.filter(
                        title__iregex=name,
                        price__range=(min_price, max_price),
                        count__gt=0,
                        freeDelivery=True,
                        tags__in=tags,
                    ).prefetch_related("images", "tags")
                ).distinct()
            else:
                catalog = catalog.filter(
                    title__iregex=name,
                    price__range=(min_price, max_price),
                    count__gt=0,
                    freeDelivery=True,
                ).prefetch_related("images")
        elif tags:
            catalog = (
                catalog.filter(
                    title__iregex=name,
                    price__range=(min_price, max_price),
                    count__gt=0,
                    tags__in=tags,
                )
                .prefetch_related("images", "tags")
                .distinct()
            )
        else:
            catalog = catalog.filter(
                title__iregex=name, price__range=(min_price, max_price), count__gt=0
            ).prefetch_related("images")
    elif freeDelivery == "true":
        if tags:
            catalog = (
                catalog.filter(
                    title__iregex=name,
                    price__range=(min_price, max_price),
                    freeDelivery=True,
                    tags__in=tags,
                )
                .prefetch_related("images", "tags")
                .distinct()
            )
        else:
            catalog = catalog.filter(
                title__iregex=name,
                price__range=(min_price, max_price),
                freeDelivery=True,
            ).prefetch_related("images")
    elif tags:
        catalog = (
            catalog.filter(
                title__iregex=name, price__range=(min_price, max_price), tags__in=tags
            )
            .prefetch_related("images", "tags")
            .distinct()
        )
    else:
        catalog = catalog.filter(
            title__iregex=name, price__range=(min_price, max_price)
        ).prefetch_related("images")

    return catalog


class Catalog(APIView):
    def get(self, request: Request):
        products = filter_catalog(request)
        products = sort_products(request, products)
        serialized = ProductSerializer(products, many=True)
        return Response({"items": serialized.data})
