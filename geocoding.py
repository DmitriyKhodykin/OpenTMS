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
    """Return Latitude, longitude and Kladr 25-symbol street-code, e.g:
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

    try:
        request = requests.request("POST", url, data=payload,
                                   headers=headers, timeout=3.0)
    except requests.exceptions.ReadTimeout as e:
        print(f'error: ReadTimeout')
        request = None

    # Service request
    if request is not None and request.status_code == 200:
        try:
            response = json.loads(request.text, encoding='utf-8')
        except json.decoder.JSONDecodeError:
            print('error: DaData JSONDecoding')
            response = None

        try:
            geo_point = response[0]

            # Latitude and Longitude
            lat = float(geo_point["geo_lat"])
            lon = float(geo_point["geo_lon"])

            # Kladr street-code
            kladr = geo_point["street_kladr_id"]

            if len(kladr) != 25:
                delta = 25 - len(kladr)  # 25-symbol is needed
                kladr_appended = int(kladr + ('0' * delta))
            else:
                kladr_appended = kladr

            return [lat, lon, kladr_appended]

        except (TypeError, IndexError, KeyError):
            print('error: Address not found or does not exist')

    else:
        print('error: Request DaData code != 200', request.text)


if __name__ == "__main__":

    # Geopoint name
    ADDRESS = "воронеж труда 11"

    # Result: [51.6813317, 39.1823317, 3600000100009020000000000]
    coordinates = geocoding(ADDRESS)
    print('Result:', coordinates)
