from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import os
from pathlib import Path
import json
from mainapp.models import Product, ProductCategory
from django.conf import settings
import random
from basketapp.models import Basket

BASE_DIR = Path(__file__).resolve().parent.parent

menu = [
        {'href': 'main', 'name': 'Главная'},
        {'href': 'products:products', 'name': 'Продукты'},
        {'href': 'contact', 'name': 'Контакты'},
    ]

def products(request, pk=None):
    links_menu = ProductCategory.objects.filter(is_active=True)
    basket = get_basket(request.user)
    page = request.GET.get('p',1)
    print(page)
    if pk is not None:
        if pk == 0:
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
                'title': 'Продукты',
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
                'basket': basket,
                'menu': menu,

            }
        return render(request,'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'menu': menu,
        'products': same_products,
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
