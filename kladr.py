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
        try:
            request_region = requests.get(f'https://kladr-api.ru/api.php'
                                          f'?query={self.region_name}'
                                          f'&contentType=region')
            response_region = json.loads(request_region.text)
            region_code = response_region['result'][1]['id']

        # except json.decoder.JSONDecodeError:
        #     print('Ошибка кодировки ответа для кода региона')
        #     region_code = None

        except IndexError:
            print('Не удалось найти наименование региона')
            region_code = None

        return region_code

    def get_city_code(self) -> str:
        """Возвращает код города
        """
        try:
            request_city = requests.get(f'https://kladr-api.ru/api.php'
                                        f'?query={self.city_name}'
                                        f'&contentType=city'
                                        f'&regionId={self.get_region_code()}')
            response_city = json.loads(request_city.text)
            city_code = response_city['result'][1]['id']

        except IndexError:
            print('Не удалось найти наименование города')
            city_code = None

        return city_code

    def get_street_code(self) -> str:
        """Возвращает код улицы
        """
        try:
            request_street = requests.get(f'https://kladr-api.ru/api.php'
                                          f'?query={self.street_name}'
                                          f'&contentType=street'
                                          f'&regionId={self.get_region_code()}'
                                          f'&cityId={self.get_city_code()}')
            response_street = json.loads(request_street.text)
            street_code = response_street['result'][1]['id']

            # Сервис "Деловых Линий" требует длину кода в 24 символа
            if len(street_code) != 25:
                tail_code = 25 - len(street_code)
                append_street_code = str(street_code) + str(tail_code * '0')
            else:
                append_street_code = street_code

        except IndexError:
            print('Не удалось найти наименование улицы')
            append_street_code = None

        return append_street_code


if __name__ == '__main__':
    # Передаем в экземпляр класса Область, Город, Улицу
    full_code = Kladr('Санкт-Петербург', 'Санкт-Петербург', 'Рыбацкий')
    arrival_code = full_code.get_street_code()
    print(arrival_code)  # 3600000100001910000000000
