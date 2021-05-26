from django.db import models


class Orders(models.Model):
    """Input from form Orders"""
    arrival_date = models.DateField('arrival_date')
    address = models.CharField('address', max_length=256)
    cargo = models.CharField('cargo', max_length=256)
    weight = models.IntegerField('weight')
    user = models.CharField('user', max_length=64)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
