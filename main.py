from auth import auth
from geocoding import Geocoding

access_token = auth.mapbox_token

gc = Geocoding(access_token)

city_a = 'Воронеж, Россия'
city_b = 'Новосибирск, Россия'

# Определение координат
coordinates_a = gc.get_coordinates(city_a)
print(f'Координаты города <{city_a}>:', coordinates_a)
coordinates_b = gc.get_coordinates(city_b)
print(f'Координаты города <{city_b}>:', coordinates_b)

# Определение расстояния
dist = gc.distance_mapbox(city_a, city_b)
print('Расстояние между городами, км:', dist)
