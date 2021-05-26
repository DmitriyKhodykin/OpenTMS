from .models import Orders
from django.forms import ModelForm, TextInput, DateInput


class OrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = ["arrival_date", "address", "cargo", "weight", "user"]

        widgets = {
            "arrival_date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': '2021-05-20'
            }),
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
            }),
            "user": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'user@domen.org'
            })
        }
