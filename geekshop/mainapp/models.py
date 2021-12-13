from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name="имя", max_length=64, unique=True)
    description = models.CharField(verbose_name="описание",max_length=1024, blank=True, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="имя продукта", max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(verbose_name="краткое описание товара",max_length=60, blank=True, null=True)
    description = models.TextField(verbose_name="описание товара", max_length=260, blank=True, null=True)
    price = models.DecimalField(verbose_name="цена продукта", max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name="кол-во на складе", default=0)
    def __str__(self):
        return f"{self.name} ({self.category.name})"
