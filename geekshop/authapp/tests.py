from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.test.client import Client


# Create your tests here.

class UserTestCase(TestCase):
    username = 'admin'
    email = 'madmax@pretty.com'
    password = 'admin'

    new_user_data = {
        'username': 'django1',
        'first_name': 'django1',
        'last_name': 'django1',
        'email': 'django1@mail.ru',
        'password1': 'Geekshop1231_',
        'password2': 'Geekshop1231_',
        'age': 31,
    }

    def setUp(self) -> None:
        self.user = ShopUser.objects.create_superuser(self.username,self.email,self.password)
        self.client = Client()


    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.client.login(username=self.username,password=self.password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 302)

    def test_register(self):

        response = self.client.post('/auth/register/',data=self.new_user_data)
        print(response.status_code)

        self.assertEqual(response.status_code, 302)

        user = ShopUser.objects.get(username=self.new_user_data['username'])
        # verify / < str: email > / < str: activate_key > /
        activation_url = f"{settings.DOMAIN_NAME}/auth/verify/{user.email}/{user.activation_key}/"

        response = self.client.get(activation_url)

        self.assertEqual(response.status_code,302)
        self.assertFalse(user.is_active)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

class SigninTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='bot', password='bot', email='test@example.com')
        self.user.save()
    def tearDown(self):
        self.user.delete()
    def test_correct(self):
        user = authenticate(username='bot', password='bot')
        self.assertTrue((user is not None) and user.is_authenticated)
    def test_wrong_username(self):
        user = authenticate(username='wrong', password='bot')
        self.assertFalse(user is not None and user.is_authenticated)
    def test_wrong_pssword(self):
        user = authenticate(username='bot', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)