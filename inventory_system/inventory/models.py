from accounts.models import User
from django.db import models


class Products(models.Model):
    ProductID = models.BigIntegerField(unique=True)
    ProductCode = models.CharField(max_length=255, unique=True)
    ProductName = models.CharField(max_length=255)
    ProductImage = models.ImageField(upload_to="uploads/", blank=True, null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUser = models.ForeignKey(User, related_name="products_created", on_delete=models.CASCADE)
    IsFavourite = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    HSNCode = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "products_product"
        unique_together = (("ProductCode", "ProductID"),)
        ordering = ("-CreatedDate", "ProductID")
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.ProductName


class Size(models.Model):
    size = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "products_size"

    def __str__(self):
        return self.size


class Color(models.Model):
    color = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "products_color"

    def __str__(self):
        return self.color


class SubVariant(models.Model):
    product = models.ForeignKey(Products, related_name='subvariants', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='size_subvariants', on_delete=models.CASCADE)
    color = models.ForeignKey(Color, related_name='color_subvariants', on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = "product_subvariant"

    def __str__(self):
        return (
            f'{self.product.ProductName} | Size: {self.size.size} | Color: {self.color.color} | Stock: {self.stock}'
        )
