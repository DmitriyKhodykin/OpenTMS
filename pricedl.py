"""Модуль для получения стоимости рейса для сборного груза.

Описание методов API для работы с сервисом:
https://dev.dellin.ru/api/calculation/calculator/
"""

import requests
import json
from auth import auth
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

    def get_ltl_price(self, adress_a: str, adress_b: str,
                      count: int) -> float:
        """
        adress:
        'Россия, Воронежская, Воронеж, Остужева, 10'
        * адреса доставки - в пределах РФ (Кроме г.Калининграда),
        - count = количество грузовых мест
        """
        derival = Kladr(adress_a)
        derival_street = derival.get_street_code()
        arrival = Kladr(adress_b)
        arrival_street = arrival.get_street_code()

        # Параметры груза (гофрокороб 20 кг)
        length: float = 0.38
        width: float = 0.29
        height: float = 0.23
        weight: float = 20.0
        vol = length * width * height * count
        total_weight = float(weight * count)

        # Параметры сроков отправки груза
        produce_date = "2021-04-20"

        payload_calc = f'''
        {{
            "appkey": "{self.token}",
            "delivery": {{
                "arrival": {{
                    "address": {{
                        "street": "{arrival_street}"
                    }},
                    "variant": "address",
                    "time": {{
                        "worktimeStart": "9:30",
                        "worktimeEnd": "19:00",
                        "exactTime": "false"
                    }},
                    "handling": {{
                        "freightLift": true,
                        "toFloor": 2,
                        "carry": 50
                    }},
                    "requirements": [
                        "0x92fce2284f000b0241dad7c2e88b1655"
                    ]
                }},
                "deliveryType": {{
                    "type": "auto"
                }},
                "derival": {{
                    "produceDate": "{produce_date}",
                    "address": {{
                        "street": "{derival_street}"
                    }},
                    "variant": "address",
                    "time": {{
                        "worktimeEnd": "12:30",
                        "worktimeStart": "08:30",
                        "exactTime": "false"
                    }},
                    "handling": {{
                        "freightLift": true,
                        "toFloor": 2,
                        "carry": 50
                    }},
                    "requirements": [
                        "0x92fce2284f000b0241dad7c2e88b1655"
                    ]
                }},
                "packages": [
                    {{
                        "uid": "0x947845D9BDC69EFA49630D8C080C4FBE",
                        "count": 1
                    }}
                ]
            }},
            "members": {{
                "requester": {{
                    "uid": "ae62f076-d602-4341-b691-45bf8dfe4a10",
                    "role": "sender"
                }}
            }},
            "payment": {{
                "paymentCity": "7700000000000000000000000",
                "type": "noncash"
            }},
            "cargo": {{
                "totalVolume": {vol},
                "oversizedVolume": 0,
                "quantity": {count},
                "length": {length},
                "width": {width},
                "totalWeight": {total_weight},
                "oversizedWeight": 0,
                "weight": {weight},
                "freightName": "Food Ingredients",
                "height": {height}
            }}
        }}'''

        # Gets response
        response_calc = requests.request(
            'POST', 'https://api.dellin.ru/v2/calculator.json',
            headers=self.headers, data=payload_calc
        )

        try:
            response_dellin = json.loads(response_calc.text.encode('utf8'))
            price_dellin = response_dellin['data']['price']

        except json.decoder.JSONDecodeError:
            print(f'Price. Ошибка кодировщика: {response_calc.text}')
            price_dellin = None

        except KeyError:
            print(f'Price. Пустой ответ сервера: {response_calc.text}')
            price_dellin = None

        return price_dellin


if __name__ == '__main__':

    TOKEN = auth.dellin_token
    price = GetPrice(TOKEN)

    ltl_price = price.get_ltl_price(
        'Россия, Воронежская, Воронеж, Труда, 59',
        'Россия, Воронежская, Воронеж, Баррикадная, 39',
        1
    )

    print(ltl_price)
