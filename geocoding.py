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
    if request.status_code == 200:
        try:
            response = json.loads(request.text, encoding='utf-8')
        except json.decoder.JSONDecodeError:
            response = None
            print('error: JSONDecoding received unexpected value')

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
            print('error Index or Key: Address not found or does not exist')
    else:
        print('error: Request code != 200')


if __name__ == "__main__":

    # Geopoint name
    ADDRESS = "воронеж труда 11"

    # Result: [51.6813317, 39.1823317, 3600000100009020000000000]
    coordinates = geocoding(ADDRESS)
    print('Result:', coordinates)
