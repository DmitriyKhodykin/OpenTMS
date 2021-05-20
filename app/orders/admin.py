from django.contrib import admin
from .models import Orders


class OrdersAdmin(admin.ModelAdmin):
    """Details for Orders admin panel"""
    list_display = ('arrival_date', 'address', 'cargo', 'weight')


admin.site.register(Orders, OrdersAdmin)
