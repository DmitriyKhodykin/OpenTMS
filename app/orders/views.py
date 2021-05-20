from django.shortcuts import render, redirect
from .models import Route
from .forms import OrderForm


def index(request):

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


def signin(request):
    return render(request, 'orders/signin.html')


def result(request):
    route = Route.objects.order_by('orderby_coordinates')
    return render(request, 'orders/result.html', {'route': route})


def info(request):
    return render(request, 'orders/info.html')


def success(request):
    return render(request, 'orders/success.html')
