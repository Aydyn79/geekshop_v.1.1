from time import time

from django.core.management.base import BaseCommand
from mainapp.models import Product
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        # products = Product.objects.filter(
        #     Q(category__name='дом') | Q(id=166))
        # products = Product.objects.filter(
        #     Q(name='КупецЪ') | ~Q(category__name='классика'))
        products = Product.objects.filter(
            Q(name__contains='Комфорт'))
        # products = Product.objects.filter(
        #     ~Q(category__name='офис'))
        print(products)
