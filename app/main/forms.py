from .models import Orders
from django.forms import ModelForm


class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ["address", "cargo", "weight"]


