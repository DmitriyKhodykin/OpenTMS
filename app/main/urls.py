from django.urls import path
from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('order', views.index, name='order'),
    path('info', views.info, name='info'),
    path('result', views.result, name='result'),
    path('success', views.success, name='success')
]
