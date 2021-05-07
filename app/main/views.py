from django.shortcuts import render
from .models import Route


def index(request):
    return render(request, 'main/index.html')


def signin(request):
    return render(request, 'main/signin.html')


def result(request):
    route = Route.objects.all()
    return render(request, 'main/result.html', {'route': route})


def info(request):
    return render(request, 'main/info.html')
