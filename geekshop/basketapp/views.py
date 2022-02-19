from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.db.models import F,Q
from basketapp.models import Basket
from mainapp.models import Product

@login_required
# def basket_add(request,id):
def basket_add(request, pk):
    user_select = request.user
    # product = Product.objects.get(id=id)
    product = Product.objects.get(pk=pk)
    baskets = Basket.objects.filter(user=user_select,product=product)
    if baskets:
        basket = baskets.first()
        basket.quantity +=1
        basket.save()
        update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        print(f'basket_add {update_queries} ')
    else:
        Basket.objects.create(user=user_select,product=product,quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# @login_required
# def basket_add(request,id):
#     if request.is_ajax():
#         user_select = request.user
#         product = Product.objects.get(id=id)
#         baskets = Basket.objects.filter(user=user_select,product=product)
#         if baskets:
#             basket = baskets.first()
#             basket.quantity +=1
#             basket.save()
#         else:
#             Basket.objects.create(user=user_select,product=product,quantity=1)
#         products = Product.objects.all()
#         context = {'products': products}
#         result = render_to_string('mainapp/includes/card.html', context)
#         return JsonResponse({'result': result})

@login_required
# def basket_remove(request,basket_id):
def basket_remove(request,pk):
    # Basket.objects.get(id=basket_id).delete()
    Basket.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_edit(request,pk,quantity):
    if request.is_ajax():
        basket = Basket.objects.get(pk=pk)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets':baskets}
        result = render_to_string('basketapp/basket.html',context)
        test = JsonResponse({'result':result})
        return test



'''@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    content = {
        'title': title,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/basket.html', content)

@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    product_item = get_object_or_404(Product, pk=pk)
    basket_item = Basket.objects.filter(product=product_item, user=request.user).first()
    if not basket_item:
        basket_item = Basket(user=request.user, product=product_item)
    basket_item.quantity += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.get(pk=int(pk))

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()
        else:
            new_basket_item.delete()

        basket_items = Basket.objects.filter(user=request.user).order_by('product__category')

        content = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc_basket_list.html', content)

        return JsonResponse({'result': result})'''