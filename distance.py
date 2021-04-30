"""Distance module.

Calculates the distance between two geographic points
[lon, lat] > [lon, lat].

To solve this problem, the service is used: MapBox.com

API docs: https://docs.mapbox.com/api/overview/
"""

import json
import requests

from auth import auth
from geocoding import geocoding


def distance_mapbox(point_from: str, point_to: str,
                    profile='driving-traffic') -> int:
    """Distance between from and to returns (in km)
        # Profiles:
        # - driving-traffic
        # - driving
        # - walking
        # - cycling
    """
    # Reversing Latitude and Longitude for MapBox
    coordinates_from: list = geocoding(point_from)[0:2]
    geopoint_from: str = f'{coordinates_from[1]},{coordinates_from[0]}'  # Reverse order for MapBox
    coordinates_to: list = geocoding(point_to)[0:2]
    geopoint_to: str = f'{coordinates_to[1]},{coordinates_to[0]}'

    request = requests.get(
        f'https://api.mapbox.com/directions/v5/mapbox/{profile}/{geopoint_from};'
        f'{geopoint_to}?access_token={auth.mapbox_token}').text

    response = json.loads(request)
    distance = int(response['routes'][0]['distance']) // 1000

    return distance


if __name__ == "__main__":
    distance_between_points = distance_mapbox("Воронеж Труда 11", "Воронеж Патриотов 11")
    print('Distance:', distance_between_points, 'km')
