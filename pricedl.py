"""Модуль для получения стоимости рейса для сборного груза.

Описание методов API для работы с сервисом:
https://dev.dellin.ru/api/calculation/calculator/
"""

import requests
import json
import datetime
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

        # Параметры сроков отправки груза
        today = datetime.date.today()
        delta = datetime.timedelta(days=3, hours=0, minutes=0)
        produce_date = "2021-04-19"  # today + delta  # "2021-04-17"

        payload_calc = f'''
        {{
            "appkey": "{self.token}",
            "delivery": {{
                "arrival": {{
                    "address": {{
                        "street": "7700000000003690000000000"
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
                    "produceDate": "2021-04-19",
                    "address": {{
                        "street": "7800000000012110000000000"
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
                "totalVolume": 0.1,
                "oversizedVolume": 0,
                "quantity": 1,
                "length": 0.54,
                "width": 0.39,
                "totalWeight": 10,
                "oversizedWeight": 0,
                "weight": 10,
                "freightName": "Food Ingredients",
                "height": 0.39
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

        except KeyError:
            response_dellin = json.loads(response_calc.text.encode('utf8'))
            price_dellin = f'Ошибка, ответ сервера: {response_dellin}'

        except json.decoder.JSONDecodeError:
            price_dellin = f'Ошибка, ответ сервера: {response_calc.text}'

        return price_dellin


if __name__ == '__main__':

    TOKEN = auth.dellin_token
    price = GetPrice(TOKEN)

    ltl_price = price.get_ltl_price(
        'Воронежская', 'Воронеж', 'Сибиряков',
        'Воронежская', 'Воронеж', 'Остужева',
        20, 2
    )

    print('Стоимость доставки сборного груза', ltl_price, 'руб.')
