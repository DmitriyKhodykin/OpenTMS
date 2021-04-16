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

    def get_region_code(self) -> str:
        """Возвращает код региона
        """
        request_region = requests.get(f'https://kladr-api.ru/api.php'
                                      f'?query={self.region_name}'
                                      f'&contentType=region')
        response_region = json.loads(request_region.text)
        region_code = response_region['result'][1]['id']

        return region_code

    def get_city_code(self) -> str:
        """Возвращает код города
        """
        request_city = requests.get(f'https://kladr-api.ru/api.php'
                                    f'?query={self.city_name}'
                                    f'&contentType=city'
                                    f'&regionId={self.get_region_code()}')
        response_city = json.loads(request_city.text)
        city_code = response_city['result'][1]['id']

        return city_code

    def get_street_code(self) -> str:
        """Возвращает код улицы
        """
        request_street = requests.get(f'https://kladr-api.ru/api.php'
                                      f'?query={self.street_name}'
                                      f'&contentType=street'
                                      f'&regionId={self.get_region_code()}'
                                      f'&cityId={self.get_city_code()}')
        response_street = json.loads(request_street.text)
        street_code = response_street['result'][1]['id']

        # Сервис "Деловых Линий" требует длину кода в 24 символа
        if len(street_code) != 24:
            tail_code = 24 - len(street_code)
            append_street_code = str(street_code) + str(tail_code * '0')
        else:
            append_street_code = street_code

        return append_street_code


if __name__ == '__main__':
    # Передаем в экземпляр класса Область, Город, Улицу
    full_code = Kladr('Воронежская', 'Воронеж', 'Остужева')
    arrival_code = full_code.get_street_code()
    print(arrival_code)  # 360000010000191000000000
