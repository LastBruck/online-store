from django.urls import path
from .views import (
    TagsList,
    ProductDetail,
    LimitedList,
    PopularList,
    SalesList,
    CreateReview,
    CategoriesList,
    BannersList,
    Catalog,
)

urlpatterns = [
    path("catalog/", Catalog.as_view(), name="products_list"),
    path("banners/", BannersList.as_view(), name="banners"),
    path("categories/", CategoriesList.as_view(), name="categories"),
    path("products/popular/", PopularList.as_view(), name="popular"),
    path("products/limited/", LimitedList.as_view(), name="limited"),
    path("sales/", SalesList.as_view(), name="sales"),
    path("product/<int:pk>/", ProductDetail.as_view(), name="product_detail"),
    path("product/<int:pk>/reviews", CreateReview.as_view(), name="add_reviews"),
    path("tags/", TagsList.as_view(), name="tags_list"),
]
