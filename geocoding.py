"""Geocoding module.

The task of direct geocoding is to obtain coordinates (latitude and longitude)
of a geographic point by its name.

To solve this problem, the service is used: DaData.ru

API docs: https://dadata.ru/api/geocode/
"""

import json             # Работа с JSON
import requests         # HTTP-запросы
from auth import auth   # Регистрационные данные


def geocoding(address: str) -> list:
    """Latitude and longitude returns [0], and Kladr 25-symbol street-code, e.g:
    [38.05, 41.06, 3600000100006660000000000].
    """
    url = "https://cleaner.dadata.ru/api/v1/clean/address"

    address = f'[ "{address}" ]'

    payload = address.encode('utf-8')

    # Request params
    headers = {
        'authorization': auth.da_token,
        'x-secret': auth.da_secret,
        'content-type': "application/json",
        'cache-control': "no-cache"
    }

    request = requests.request("POST", url, data=payload, headers=headers)

    # Service response
    response = json.loads(request.text, encoding='utf-8')
    geo_point = response[0]

    # Latitude and Longitude
    lat = float(geo_point["geo_lat"])
    lon = float(geo_point["geo_lon"])

    #Kladr street-code
    kladr = geo_point["street_kladr_id"]
    if len(kladr) != 25:
        delta = 25 - len(kladr)  # 25-symbol is needed
        kladr_appended = int(kladr + ('0' * delta))
    else:
        kladr_appended = kladr

    return [lat, lon, kladr_appended]


if __name__ == "__main__":

    # Geopoint name
    ADDRESS = "воронеж патриотов 11"

    # Определение координат
    coordinates = geocoding(ADDRESS)
    print('Result:', coordinates)
