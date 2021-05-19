from .models import Orders
from django.forms import ModelForm, TextInput


class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ["address", "cargo", "weight"]
        widgets = {
            "address": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Воронеж Патриотов 20'
            }),
            "cargo": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пищевые ингредиенты'
            }),
            "weight": TextInput(attrs={
                'class': 'form-control',
                'placeholder': '900'
            })
        }
