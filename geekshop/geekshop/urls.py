from django.contrib import admin
from django.urls import path
from mainapp.views import products, contact, main
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', main, name = 'main'),
    path('products/', include('mainapp.urls', namespace = 'products')),
    path('basket/', include('basketapp.urls', namespace = 'basket')),
    path('auth/', include('authapp.urls', namespace = 'auth')),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('contact', contact, name = 'contact'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)