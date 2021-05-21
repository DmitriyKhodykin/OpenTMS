from django.shortcuts import render, redirect
from .models import Route


def result(request):
    route = Route.objects.order_by('orderby_coordinates')
    return render(request, 'optimizer/result.html', {'route': route})
