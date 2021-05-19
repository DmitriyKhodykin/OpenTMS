from django.contrib import admin
from .models import Orders, Route


class OrdersAdmin(admin.ModelAdmin):
    """Details for Orders admin panel"""
    list_display = ('address', 'cargo', 'weight')

    class Meta:
        verbose_name = ('Адресс', 'Груз', 'Вес')


class RouteAdmin(admin.ModelAdmin):
    """Details for Route admin panel"""
    list_display = ('latitude', 'longitude')


admin.site.register(Orders, OrdersAdmin)
admin.site.register(Route, RouteAdmin)
