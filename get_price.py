"""Модуль для получения стоимости рейса для сборного груза.

Описание методов API для работы с сервисом:
https://dev.dellin.ru/api/calculation/calculator/
"""

import requests
import pandas as pd
import json
from auth import auth
import datetime
from kladr import Kladr


class GetPrice:
    """
    Возвращает стоимость доставки из пункта А в пункт Б в рублях.
    """

    # Defines content type
    headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self, token):
        self.token = token

    def get_ltl_price(self, reg_a: str, city_a: str, street_a: str,
                      reg_b: str, city_b: str, street_b: str,
                      weight: float, count: int) -> float:
        """
        - reg_a = регион отправления*: <Воронежская>,
        - city_a = город отправления*: <Воронеж>,
        - street_a = улица отправления: <Сибиряков>,
        - reg_b = регион доставки*: <Воронежская>,
        - city_b = город доставки*: <Воронеж>,
        - street_b = улица доставки: <Остужева>
        * адреса доставки - в пределах РФ (Кроме г.Калининграда),
        - weight = вес самого тяжелого грузового места в кг,
        - count = количество грузовых мест
        """
        derival = Kladr(reg_a, city_a, street_a)
        derival_street = derival.get_street_code()
        arrival = Kladr(reg_b, city_b, street_b)
        arrival_street = arrival.get_street_code()

        # Параметры груза
        length = 1.2
        width = 0.8
        vol = length*width*count
        total_weight = int(weight*count)

        today = datetime.date.today()
        delta = datetime.timedelta(days=3, hours=0, minutes=0)
        produce_date = today + delta

        payload_calc = f'''{{
            "appkey": "{self.token}",
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
            'POST', 'https://api.dellin.ru/v2/calculator.json',
            headers=self.headers, data=payload_calc
        )
        response_dellin = json.loads(response_calc.text.encode('utf8'))

        price_dellin = response_dellin  #['data']['price']

        return price_dellin


if __name__ == '__main__':

    TOKEN = auth.dellin_token
    price = GetPrice(TOKEN)

    ltl_price = price.get_ltl_price(
        'Воронежская', 'Воронеж', 'Сибиряков',
        'Белгородская', 'Алексеевка', 'Большевиков',
        100, 2
    )

    print('Стоимость доставки сборного груза', ltl_price, 'руб.')
