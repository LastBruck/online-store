from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=128, db_index=True)
    active = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    def href(self):
        return f"/catalog/{self.pk}"

    def __str__(self):
        return self.title


def category_image_directory_path(instance: "CategoryIcon", filename):
    return "catalog/icons/{category}/{filename}".format(
        category=instance.category,
        filename=filename,
    )


class CategoryIcon(models.Model):
    class Meta:
        verbose_name = "Category icon"
        verbose_name_plural = "Category icons"

    src = models.FileField(upload_to=category_image_directory_path)
    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="image", blank=True, null=True
    )

    def alt(self):
        return self.category.title

    def href(self):
        return self.src

    def __str__(self):
        return f"Icon: Category={self.category.title}"


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    count = models.IntegerField(default=0, null=False)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=150, null=False, blank=True)
    fullDescription = models.TextField(null=False, blank=True)
    freeDelivery = models.BooleanField(default=True)
    active = models.BooleanField(default=False)
    limited_edition = models.BooleanField(default=False)
    rating = models.DecimalField(default=0, max_digits=3, decimal_places=2, null=False)

    def __str__(self):
        return f"Product(pk={self.pk}, name={self.title!r})"

    def reviews_count(self):
        return self.reviews.count()

    def average_rating(self):
        total_reviews = self.reviews.count()
        if total_reviews > 0:
            total_rating = sum(review.rate for review in self.reviews.all())
            return total_rating / total_reviews
        return 0


def product_images_directory_path(instance: "ProductImage", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class ProductImage(models.Model):
    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="product"
    )
    name = models.CharField(max_length=100, null=False, blank=True)
    image = models.ImageField(upload_to=product_images_directory_path)

    def src(self):
        return self.image

    def alt(self):
        return self.product.title

    def __str__(self):
        return f"/{self.image}"


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=128, null=False, blank=True)
    product = models.ManyToManyField(
        Product, related_name="tags", verbose_name="product"
    )

    def __str__(self):
        return f"Tag: (Name={self.name})"


class Review(models.Model):
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    author = models.CharField(max_length=128)
    email = models.EmailField(max_length=256)
    text = models.TextField()
    rate = models.PositiveSmallIntegerField(blank=False, default=5)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="reviews",
        verbose_name="product",
    )

    def __str__(self):
        return f"Review: (Author={self.author}, product={self.product.title})"


class ProductSpecification(models.Model):
    class Meta:
        verbose_name = "Product specification"
        verbose_name_plural = "Product specifications"

    name = models.CharField(max_length=120, null=False, blank=True)
    value = models.CharField(max_length=150, null=False, blank=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="specifications",
        verbose_name="product",
    )


class Sale(models.Model):
    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    price = models.DecimalField(
        max_digits=10, db_index=True, decimal_places=2, default=0
    )
    salePrice = models.DecimalField(
        max_digits=10, db_index=True, decimal_places=2, default=0
    )
    dateFrom = models.DateField(blank=True, null=False)
    dateTo = models.DateField(blank=True, null=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sales", verbose_name="product"
    )

    def title(self):
        return self.product.title

    def href(self):
        return f"/product/{self.product.pk}"

    def __str__(self):
        return self.product.title
