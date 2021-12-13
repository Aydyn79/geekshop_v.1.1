from django.shortcuts import render, get_object_or_404
import os
from pathlib import Path
import json
from mainapp.models import Product, ProductCategory
from django.conf import settings
import random
from basketapp.models import Basket

BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.


# links_menu = [
#         {'href':'product_all', 'name':'все'},
#         {'href': 'product_home', 'name':'дом'},
#         {'href': 'product_office', 'name': 'офис'},
#         {'href': 'product_classic', 'name': 'классика'},
#     ]

menu = [
        {'href': 'main', 'name': 'Главная'},
        {'href': 'products:products', 'name': 'Продукты'},
        {'href': 'contact', 'name': 'Контакты'},
    ]



def products(request, pk=None):
    # basket = []
    # if request.user.is_authenticated:
    #     basket = sum(list(Basket.objects.filter(user=request.user).values_list('quantity', flat=True)))
    links_menu = ProductCategory.objects.all()
    basket = get_basket(request.user)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category_item = {'name': 'Все', 'pk':0}
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category=category_item).order_by('price')
        content = {
            'title': 'Продукты',
            'links_menu': links_menu,
            'menu': menu,
            'category': category_item,
            'products': products_list,
            # 'product': get_object_or_404(Product, pk=pk),
            'hot_product': hot_product,
            'same_products': same_products,
            'basket': basket
        }

        return render(request,'mainapp/products_list.html', content)
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'menu': menu,
        'products': same_products,
        # 'product': get_object_or_404(Product, pk=pk),
        'basket': basket,
        'hot_product': hot_product,
    }

    return render(request, 'mainapp/products.html', content)

def contact(request):
    with open(os.path.join(settings.BASE_DIR, 'mainapp\\json\\contact__locations.json')) as f:
        locations = json.load(f)
    content = {
        'title': 'О нас',
        'menu': menu,
        'locations':locations
    }
    return render(request,'mainapp/contact.html', content)


def main(request):
    classic = Product.objects.filter(category_id=5)
    content ={'title': 'Магазин', 'menu': menu, 'classic': classic}
    return render(request,'mainapp/index.html', content)

def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def product(request, pk):
    content = {
        'title': 'Товар',
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', content)
