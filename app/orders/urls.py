from django.urls import path
from . import views

urlpatterns = [
    path('', views.orders, name='order'),
    path('success', views.success, name='success')
]
