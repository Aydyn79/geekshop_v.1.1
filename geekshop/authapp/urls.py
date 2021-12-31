from django.urls import path, re_path
from authapp.views import ProfileFormView,LoginListView,RegisterListView,Logout

app_name ='authapp'

urlpatterns = [
    path('login/', LoginListView.as_view(), name='login'),
    path('register/', RegisterListView.as_view(), name='register'),
    path('edit/', ProfileFormView.as_view(), name='edit'),
    path('logout/', Logout.as_view(), name='logout'),

    path('verify/<str:email>/<str:activate_key>/', RegisterListView.verify, name='verify'),
]

