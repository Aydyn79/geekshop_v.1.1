from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models



class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveSmallIntegerField(verbose_name='возраст', null=True)
    email = models.CharField(('email'), max_length=50, null=False, validators=[
        EmailValidator(message='Введите корректный адрес', whitelist=['localhost', 'my_local'])
    ])
