from django.urls import reverse
from rest_framework.test import APITestCase

from orders.models import Orders
from orders.serializers import OrderSerializer


class OrderApiTest(APITestCase):
    """API test cases"""

    def test_get(self):
        """Orders Get method test"""

        order = Orders.objects.create(
            arrival_date='2022-02-22',
            address='Test',
            cargo='Test',
            weight=1,
            user='test@test.net'
        )

        url = reverse('orders-list')
        response = self.client.get(url).data
        serializer_data = OrderSerializer([order], many=True).data
        self.assertEqual(serializer_data, response)
