from django.urls import path

from . import views

urlpatterns = [
    path('', views.signin, name='signin'),
    path('info', views.info, name='info'),
]
