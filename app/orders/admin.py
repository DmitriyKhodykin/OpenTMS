from django.contrib import admin
from .models import Orders, Route


class OrdersAdmin(admin.ModelAdmin):
    """Details for Orders admin panel"""
    list_display = ('arrival_date', 'address', 'cargo', 'weight')


class RouteAdmin(admin.ModelAdmin):
    """Details for Route admin panel"""
    list_display = ('latitude', 'longitude')


admin.site.register(Orders, OrdersAdmin)
admin.site.register(Route, RouteAdmin)
