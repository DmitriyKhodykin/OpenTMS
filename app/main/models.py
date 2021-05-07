from django.db import models


class Orders(models.Model):
    order_id = models.IntegerField('order_id', default=0)
    address = models.CharField('address', max_length=256, default='Нет адреса')
    cargo = models.CharField('cargo', max_length=256, default='Нет груза')
    weight = models.IntegerField('weight', default=0)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Route(models.Model):
    """Results of the optimization module"""
    order_id = models.IntegerField('order_id', default=0)
    latitude = models.FloatField('latitude', default=0.0)
    longitude = models.FloatField('longitude', default=0.0)
    orderby_coordinates = models.IntegerField('orderby_coordinates', default=0)
    orderby_distance = models.IntegerField('orderby_distance', default=0)
    orderby_price = models.IntegerField('orderby_price', default=0)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
