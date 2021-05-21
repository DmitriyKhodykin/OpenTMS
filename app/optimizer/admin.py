from django.contrib import admin
from .models import Route


class RouteAdmin(admin.ModelAdmin):
    """Details for Route admin panel"""
    list_display = ('address', 'latitude', 'longitude', 'orderby_coordinates')


admin.site.register(Route, RouteAdmin)
