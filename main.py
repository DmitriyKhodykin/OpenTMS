from auth import auth
from geocoding import Geocoding

MAPBOX_TOKEN = auth.mapbox_token

gc = Geocoding(MAPBOX_TOKEN)

CITY_A = 'Воронеж, Россия'
CITY_B = 'Новосибирск, Россия'

# Определение координат
coordinates_a = gc.get_coordinates(CITY_A)
print(f'Координаты города <{CITY_A}>:', coordinates_a)
coordinates_b = gc.get_coordinates(CITY_B)
print(f'Координаты города <{CITY_B}>:', coordinates_b)

# Определение расстояния
dist = gc.distance_mapbox(CITY_A, CITY_B)
print('Расстояние между городами, км:', dist)
