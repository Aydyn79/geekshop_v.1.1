from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='media_folder_products')
def media_folder_products(path_to_products_images):
    if not path_to_products_images:
        path_to_products_images = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{path_to_products_images}'


@register.filter(name='media_folder_users')
def media_folder_users(path_to_users_avatars):
    if not path_to_users_avatars:
        path_to_users_avatars = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{path_to_users_avatars}'


