from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import os
from pathlib import Path
import json

from django.template.loader import render_to_string
from mainapp.models import Product, ProductCategory
from django.conf import settings
import random
from django.views.generic import DetailView
from django.conf import settings
from django.core.cache import cache
# from django.views.decorators.cache import never_cache


BASE_DIR = Path(__file__).resolve().parent.parent
MODULE_DIR = os.path.dirname(__file__)


def main(request):
    context = {
        'title': 'Geekshop', }
    return render(request, 'mainapp/index.html', context)


# def products(request, pk=None):
#     page = request.GET.get('p',1)
#     print(page)
#     if pk is not None:
#         if pk == 0:
#             category = {
#                 'pk': 0,
#                 'name': 'все'
#             }
#             # products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category').order_by('price')
#             products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category').order_by('price')
#
#         else:
#             # category = get_object_or_404(ProductCategory, pk=pk)
#             # products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
#             products = Product.objects.all().select_related()
#
#         paginator = Paginator(products, 2)
#         try:
#             products_paginator = paginator.page(page)
#         except PageNotAnInteger:
#             products_paginator = paginator.page(1)
#         except EmptyPage:
#             products_paginator = paginator.page(paginator.num_pages)
#
#         context = {
#                 'title': 'Geekshop | Каталог',
#                 'category': category,
#                 'products': products_paginator,
#                 }
#         return render(request,'mainapp/products.html', context)
#     hot_product = get_hot_product()
#     same_products = get_same_products(hot_product)
#     category = hot_product.category
#     context = {
#         'title': 'Geekshop | Каталог',
#         'category': category,
#         'products': same_products,
#
#     }
#
#     return render(request, 'mainapp/products.html', context)
# @never_cache
def products(request, id_category=None, page=1):
    context = {
        'title': 'Geekshop | Каталог',
    }

    if id_category:
        # products = Product.objects.filter(category_id=id_category).select_related('category')
        categories = get_categories()
        products = get_products_in_category_orederd_by_price(id_category)
    else:
        categories = get_categories()
        products = get_products_orederd_by_price()
        # products = Product.objects.all().select_related()
        # products = Product.objects.all().prefetch_related()
        # products = get_product()
    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context['products'] = products_paginator
    # context['categories'] = ProductCategory.objects.all()
    context['categories'] = categories
    return render(request, 'mainapp/products.html', context)


def products_ajax(request, id_category=None, page=1):
    context = {
        'title': 'Geekshop | Каталог',
    }

    if request.is_ajax():
        if id_category:
            # products = Product.objects.filter(category_id=id_category).select_related('category')
            categories = get_categories()
            products = get_products_in_category_orederd_by_price(id_category)
        else:
            categories = get_categories()
            products = get_products_orederd_by_price()
            # products = Product.objects.all().select_related()
            # products = Product.objects.all().prefetch_related()
            # products = get_product()
        paginator = Paginator(products, per_page=3)

        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context['products'] = products_paginator
        # context['categories'] = ProductCategory.objects.all()
        context['categories'] = categories
        result = render_to_string(
            'mainapp/includes/inc_products_list_content.html',
            context=context,
            request=request)

        return JsonResponse({'result': result})


def contact(request):
    with open(os.path.join(settings.BASE_DIR, 'mainapp\\json\\contact__locations.json')) as f:
        locations = json.load(f)
    menu = [
        {'href': 'main', 'name': 'Главная'},
        {'href': 'products', 'name': 'Продукты'},
        {'href': 'contact', 'name': 'Контакты'},
    ]
    content = {
        'title': 'О нас',
        'menu': menu,
        'locations': locations
    }
    return render(request, 'mainapp/contact.html', content)


# def main(request):
#     classic = Product.objects.filter(category_id=5)
#     content ={'title': 'Магазин', 'menu': menu, 'classic': classic}
#     return render(request,'mainapp/index.html', content)

# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     else:
#         return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


# def product(request, pk):
#     content = {
#         'title': 'Товар',
#         'links_menu': ProductCategory.objects.all(),
#         'product': get_object_or_404(Product, pk=pk),
#
#     }
#
#     return render(request, 'mainapp/product.html', content)

class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        product = self.get_object()
        context['product'] = product
        return context


# половина кэшей не нужна
# def get_links_menu():
#     if settings.LOW_CACHE:
#         key = 'links_menu'
#         links_menu = cache.get(key)
#         if links_menu is None:
#             links_menu = ProductCategory.objects.filter(is_active=True)
#             cache.set(key, links_menu)
#         return links_menu
#     else:
#         return ProductCategory.objects.filter(is_active=True)
#
#
# def get_category(pk):
#     if settings.LOW_CACHE:
#         key = f'category_{pk}'
#         category = cache.get(key)
#         if category is None:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             cache.set(key, category)
#         return category
#     else:
#         return get_object_or_404(ProductCategory, pk=pk)


def get_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.filter(is_active=True)
            cache.set(key, categories)
        return categories
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


# def get_product(pk):
#     if settings.LOW_CACHE:
#         key = f'product_{pk}'
#         product = cache.get(key)
#         if product is None:
#             product = get_object_or_404(Product, pk=pk)
#             cache.set(key, product)
#         return product
#     else:
#         return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
