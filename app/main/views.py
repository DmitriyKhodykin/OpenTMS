from django.http import HttpResponse


def index(request):
    return HttpResponse("<h4>Hi There!</h4>")


def about(request):
    return HttpResponse("<h4>We are strong!</h4>")
