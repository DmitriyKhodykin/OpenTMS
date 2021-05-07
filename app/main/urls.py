from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('info', views.info, name='info'),
    path('result', views.result, name='result'),
    path('signin', views.signin, name='signin')
]
