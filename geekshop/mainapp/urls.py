from django.urls import path
from mainapp.views import products, ProductDetail


app_name ='mainapp'

urlpatterns = [
    # path('', mainapp.products, name='products'),
    # path('category/<int:pk>/', mainapp.products, name='category'),
    # # path('<int:pk>/', mainapp.products, name='category'),
    # # path('category/<int:pk>/page/<int:page>/', mainapp.products, name='page'),
    # path('product/<int:pk>/', mainapp.product, name='product'),
    path('', products,name='products'),
    path('category/<int:id_category>', products, name='category'),
    path('page/<int:page>', products, name='page'),
    path('detail/<int:pk>/', ProductDetail.as_view(), name='detail'),
]


