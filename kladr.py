"""Модуль для получения кода адреса по классификатору КЛАДР.

Для получения токена необходима регистрация в сервисе: https://kladr-api.ru/
Параметры запроса к API: https://kladr-api.ru/docs
"""

import requests
import json


class Kladr:
    """
    Возвращает КЛАДР-коды географических объектов, таких как:
    регион, город, улица.
    """

    def __init__(self, region_name: str, city_name: str, street_name: str):
        self.region_name = region_name
        self.city_name = city_name
        self.street_name = street_name

    def get_region_code(self):
        """Возвращает код региона
        """
        request_region = requests.get(f'https://kladr-api.ru/api.php?query={self.region_name}'
                                      f'&contentType=region')
        response_region = json.loads(request_region.text)
        region_code = response_region['result'][1]['id']

        return region_code

    def get_city_code(self):
        """Возвращает код города
        """
        request_city = requests.get(f'https://kladr-api.ru/api.php?query={self.city_name}'
                                    f'&contentType=city'
                                    f'&regionId={self.get_region_code()}')
        response_city = json.loads(request_city.text)
        city_code = response_city['result'][1]['id']

        return city_code

    def get_street_code(self) -> int:
        """Возвращает код улицы
        """
        request_street = requests.get(f'https://kladr-api.ru/api.php?query={self.street_name}'
                                      f'&contentType=street'
                                      f'&regionId={self.get_region_code()}'
                                      f'&cityId={self.get_city_code()}')
        response_street = json.loads(request_street.text)
        street_code = response_street['result'][1]['id']

        return street_code


if __name__ == '__main__':
    full_code = Kladr('Воронежская', 'Воронеж', 'Сибиряков')
    arrival_code = full_code.get_street_code()
    print(arrival_code)  # 36000001000019100
