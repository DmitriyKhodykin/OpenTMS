from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('order', views.orders, name='order'),
    path('info', views.info, name='info'),
    path('success', views.success, name='success')
]
