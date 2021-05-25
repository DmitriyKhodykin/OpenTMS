from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet

from .forms import OrderForm
from .models import Orders
from .serializers import OrderSerializer


def orders(request):

    error = ''

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            error = 'Проверьте корректность заполнения формы'

    form = OrderForm()

    context = {
        'form': form,
        'error': error
    }

    return render(request, 'orders/index.html', context)


def success(request):
    return render(request, 'orders/success.html')


class OrderView(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
