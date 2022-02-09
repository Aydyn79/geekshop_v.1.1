from django.contrib import admin
from django.urls import path, re_path
from mainapp.views import products, contact, main
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
import debug_toolbar
from django.views.i18n import set_language

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', main, name = 'main'),
    path('products/', include('mainapp.urls', namespace = 'products')),
    path('basket/', include('basketapp.urls', namespace = 'basket')),
    path('auth/', include('authapp.urls', namespace = 'auth')),
    path('admin/', include('adminapp.urls', namespace='admin')),
    path('contact', contact, name = 'contact'),
    path('orders/', include('ordersapp.urls', namespace='orders')),

    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    path('', include('social_django.urls', namespace='social')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('debug', include(debug_toolbar.urls))]