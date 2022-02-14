from django.conf import settings
from django.db import models
# from django.utils.functional import cached_property
from mainapp.models import Product




class BasketQuerySet(models.QuerySet):

   def delete(self, *args, **kwargs):
       for object in self:
           object.product.quantity += object.quantity
           object.product.save()
       super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(verbose_name='количество', default=0)
    add_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='время')
    update_timestamp = models.DateTimeField(auto_now=True)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для  {self.user.username} | Продукт{self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    # Methods
    # обновление инфы о стоимости и количестве даже визуально замедляется
    # поэтому я закоментил этот способ кэширования
    # @cached_property
    # def get_items_cached(self):
    #     return self.user.basket.select_related()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        "return total quantity for user"
        # _items = self.get_items_cached
        _items = Basket.objects.filter(user=self.user)
        # print(_items)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))

        return _totalquantity

    @property
    def total_cost(self):
        "return total cost for user"
        _items = Basket.objects.filter(user=self.user)
        # _items = self.get_items_cached
        # print(_items)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))

        return _totalcost

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.save()
        super(Basket, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

    def get_item (instance_id):
        return Basket.objects.get(id=instance_id)


