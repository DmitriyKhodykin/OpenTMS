"""Модуль для загрузки справочников городов и улиц.

API KLADR https://dev.dellin.ru/api/catalogs/places/
"""

import json             # Работа с JSON
import pandas as pd     # Таблицы и фильтры
import requests         # HTTP-запросы
from auth import auth   # Регистрационные данные


class KladrLoader:
    """Загружает справочники городов и улиц через API dellin"""

    def __init__(self, access_token: str):
        self.access_token = access_token

        self.headers = {
            'Content-Type': 'application/json'
        }

        self.payload_link = f'''{{
            "appkey": "{self.access_token}"
        }}'''

    def cities_loader(self) -> pd.DataFrame:
        """Загружает справочник городов"""

        response_cities = requests.request(
            'POST', 'https://api.dellin.ru/v1/public/places.json',
            headers=self.headers, data=self.payload_link
        )
        csv_link = json.loads(response_cities.text.encode('utf8'))
        print('Загрузка каталога городов')
        cities = pd.read_csv(csv_link['url'])
        return cities

    def streets_loader(self) -> pd.DataFrame:
        """Загружает справочник улиц"""

        response_str = requests.request(
            'POST', 'https://api.dellin.ru/v1/public/streets.json',
            headers=self.headers, data=self.payload_link
        )
        csv_link = json.loads(response_str.text.encode('utf8'))
        print('Загрузка каталога улиц')
        streets = pd.read_csv(csv_link['url'])
        return streets

    def merge_table(self) -> pd.DataFrame:
        """Объединяет таблицы улиц и городов в единую таблицу"""

        streets = self.streets_loader()
        cities = self.cities_loader()
        print('Объединение каталогов')
        catalog = streets.merge(cities, how='left', on='cityID')
        print('Сохранение общего каталога')
        catalog.to_csv('Catalog.csv')


if __name__ == "__main__":

    # Регистрационные данные для сервиса
    DELLIN_TOKEN = auth.dellin_token

    # Создание экземпляра класса
    kl = KladrLoader(DELLIN_TOKEN)

    # Загрузка и сохранение справочника
    kl.merge_table()
