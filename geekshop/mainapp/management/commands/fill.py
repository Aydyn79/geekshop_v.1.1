from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand
import json
import os

from mainapp.models import ProductCategory, Product
from django.conf import settings

from authapp.models import ShopUser


def load_from_json(file_name):
    with open(os.path.join(settings.BASE_DIR, f"mainapp/json/{file_name}.json"), 'r', encoding='utf-8') as f:
        return json.load(f)

class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all().delete()
        for cat in categories:
            ProductCategory.objects.create(**cat)
        products = load_from_json('products')
        Product.objects.all().delete()
        for prod in products:
            _cat = ProductCategory.objects.get(name=prod['category'])
            prod['category'] = _cat
            Product.objects.create(**prod)
        # shop_users = ShopUser.objects.all()
        # for uzver in shop_users:
        #     if uzver.username != "admin":
        #         uzver.delete()
        # ShopUser.objects.create_superuser('odmin','django@local.gb', 'odmin', age=18)