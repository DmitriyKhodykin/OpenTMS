from django.shortcuts import render

from optimizer.models import Route


def result(request):
    """Render result from Optimizer module"""
    route = Route.objects.order_by('orderby_coordinates')
    return render(request, 'optimizer/result.html', {'route': route})
