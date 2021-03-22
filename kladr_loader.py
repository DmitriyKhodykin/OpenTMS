# Модуль для загрузки справочников городов и улиц
# API KLADR https://dev.dellin.ru/api/catalogs/places/

import requests
import pandas as pd
import json
import auth


class KladrLoader:
    """Загружает справочники городов и улиц
    через API dllin
    """

    headers = {
        'Content-Type': 'application/json'
    }

    payload_link = f'''{{
        "appkey": "{auth.appkey_dellin}"
    }}'''

    def cities_loader(self):
        """Загружает справочник городов"""
        response_cities = requests.request(
            'POST', auth.url_cities,
            headers=self.headers, data=self.payload_link
        )
        csv_link = json.loads(response_cities.text.encode('utf8'))
        print('Загрузка каталога городов')
        cities = pd.read_csv(csv_link['url'])
        print('Сохранение каталога городов')
        cities.to_csv('cities.csv')
        print('Выполнено')

    def streets_loader(self):
        """Загружает справочник улиц"""
        response_str = requests.request(
            'POST', auth.url_str,
            headers=self.headers, data=self.payload_link
        )
        csv_link = json.loads(response_str.text.encode('utf8'))
        print('Загрузка каталога улиц')
        streets = pd.read_csv(csv_link['url'])
        print('Сохранение каталога улиц')
        streets.to_csv('streets.csv')
        print('Выполнено')


if __name__ == '__main__':

    DirLoader().cities_loader()
    DirLoader().streets_loader()
