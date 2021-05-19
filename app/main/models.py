from django.db import models


class Orders(models.Model):
    """Input from order-form data"""
    address = models.CharField('address', max_length=256)
    cargo = models.CharField('cargo', max_length=256)
    weight = models.IntegerField('weight')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Route(models.Model):
    """Results of the optimization module"""
    order_id = models.OneToOneField(Orders, on_delete=models.CASCADE, primary_key=True)
    latitude = models.FloatField('latitude', default=0.0)
    longitude = models.FloatField('longitude', default=0.0)
    orderby_coordinates = models.IntegerField('orderby_coordinates', default=0)
    orderby_distance = models.IntegerField('orderby_distance', default=0)
    orderby_price = models.IntegerField('orderby_price', default=0)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
