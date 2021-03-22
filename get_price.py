# Модуль для получения данных о стоимости рейса по доставке сборного груза
# API  https://dev.dellin.ru/api/calculation/calculator/

import requests
import pandas as pd
from prettytable import PrettyTable
import json
import auth
import datetime


class GetPrice:

    # Defines content type
    headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self, ltl=True):
        self.ltl = ltl

    def get_street_id(self, reg, city, street):
        """Возвращает код улицы населенного пункта
        в соответствии с классификатором адресов РФ (КЛАДР),
        например, 100000100000010000000000.
        - reg = наименование региона: <Адыгея>,
        - city = наименование города: <Майкоп>,
        - street = наименование улицы: <Абадзехская>"""

        df_cities = pd.read_csv('cities.csv')
        df_streets = pd.read_csv('streets.csv')

        city_id = df_cities[(df_cities['regname'].str.contains(reg))
                            & (df_cities['name'].str.contains(city))]['cityID'].values[0]

        street_id = df_streets[(df_streets['cityID'] == city_id)
                               & (df_streets['name'].str.contains(street))]['code'].values[0]
        return street_id

    def get_ltl_price(self, reg_a, city_a, street_a,
                      reg_b, city_b, street_b, weight, count):
        """GetPrice(reg_a, city_a, street_a, reg_b, city_b, street_b, weight, count):
        - reg_a = регион отправления*: <Воронежская>,
        - city_a = город отправления*: <Воронеж>,
        - street_a = улица отправления: <Сибиряков>,
        - reg_b = регион доставки*: <Воронежская>,
        - city_b = город доставки*: <Воронеж>,
        - street_b = улица доставки: <Остужева>
        * адреса доставки - в пределах РФ (Кроме г.Калининграда),
        - weight = вес самого тяжелого грузового места в кг,
        - count = количество грузовых мест"""

        derival_street = self.get_street_id(reg_a, city_a, street_a)
        arrival_street = self.get_street_id(reg_b, city_b, street_b)

        # Requests data
        length = 1.2
        width = 0.8
        vol = length*width*count
        total_weight = int(weight*count)

        today = datetime.date.today()
        delta = datetime.timedelta(days=3, hours=0, minutes=0)
        produce_date = today + delta

        payload_calc = f'''{{
            "appkey": "{auth.appkey_dellin}",
            "delivery": {{
                "deliveryType": {{
                    "type": "auto"
                }},
                "arrival": {{
                    "variant": "address",
                    "address":{{
                        "street":{arrival_street}
                    }},
                    "time": {{
                        "worktimeStart": "8:00",
                        "worktimeEnd": "17:00",
                        "breakStart": "12:00",
                        "breakEnd": "13:00",
                        "exactTime": false
                    }}
                }},
                "derival": {{
                    "produceDate": "{produce_date}",
                    "variant": "address",
                    "address":{{
                        "street":{derival_street}
                    }},
                    "time": {{
                        "worktimeEnd": "23:59",
                        "worktimeStart": "00:00",
                        "breakStart": "12:00",
                        "breakEnd": "13:00",
                        "exactTime": false
                    }}
                }}
            }},
            "members": {{
                "requester": {{
                    "role": "sender"
                }}
            }},
            "cargo": {{
                "length": {length},
                "width": {width},
                "weight": {weight},
                "height": 1,
                "totalVolume": {vol},
                "totalWeight": {total_weight},
                "oversizedWeight":1,
                "oversizedVolume":1,
                "freightName":"Food",
                "hazardClass": 0
            }},
            "payment": {{
                "paymentCity": "7700000000000000000000000",
                "type": "noncash"
            }}
        }}'''

        # Gets response
        response_calc = requests.request(
            'POST', auth.url_calc,
            headers=self.headers, data=payload_calc
        )
        price_dellin = json.loads(response_calc.text.encode('utf8'))

        # Creates output table
        x = PrettyTable()
        x.field_names = ["Параметр", "Значение"]
        x.add_row(["Дата прайса", price_dellin['metadata']['generated_at']])
        x.add_row(["Тип рейса", "LTL"])
        x.add_row(["Вид транспорта", "Авто"])
        x.add_row(["Вес / Объем", f"{total_weight}кг / {vol}м3"])
        x.add_row(["Погрузка", price_dellin['data']['derival']['terminal']])
        x.add_row(["Разгрузка", price_dellin['data']['arrival']['terminal']])
        x.add_row(["Прайс с НДС", price_dellin['data']['price']])

        return x


if __name__ == '__main__':
    price_delivery = GetPrice().get_ltl_price(
        'Воронежская', 'Воронеж', 'Сибиряков',
        'Белгородская', 'Алексеевка', 'Большевиков',
        100, 2
    )

    print(
        price_delivery
    )
