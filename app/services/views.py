from django.shortcuts import render


def signin(request):
    return render(request, 'services/signin.html')


def info(request):
    return render(request, 'services/info.html')
