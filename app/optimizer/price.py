"""Module for getting the cost of the flight.

API docs: https://dev.dellin.ru/api/calculation/calculator/
"""

import requests
import json
from auth import auth
from optimizer.optimizer import geocoding


def price(address_from: str, address_to: str, count: int = 1) -> float:
    """ Return Delivery price in RUB.
    address: 'Воронеж Остужева 10'
    count = number of packages
    """
    url = 'https://api.dellin.ru/v2/calculator.json'

    derival_geocoding = geocoding(address_from)
    derival_street = derival_geocoding[2]

    arrival_geocoding = geocoding(address_to)
    arrival_street = arrival_geocoding[2]

    # Cargo parameters (static)
    length: float = 0.38
    width: float = 0.29
    height: float = 0.23
    weight: float = 20.0
    vol = length * width * height * count
    total_weight = float(weight * count)

    price_dellin = None

    # Date of shipment
    produce_date = "2021-05-11"

    # Defines content type
    headers = {
        'Content-Type': 'application/json'
    }

    payload_calc = f'''
    {{
        "appkey": "{auth.dellin_token}",
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
    try:
        request = requests.request('POST', url, headers=headers,
                                   data=payload_calc, timeout=5.0)

    except requests.exceptions.ReadTimeout:
        print('error: PricingTimeout')
        request = None

    if request is not None and request.status_code == 200:
        try:
            response_dellin = json.loads(request.text.encode('utf8'))
            price_dellin = response_dellin['data']['price']
        except json.decoder.JSONDecodeError:
            print('error: DL JSONDecodeError')
        except KeyError:
            print('error: DL Key not found')

    else:
        print('error: Request DL code != 200')

    return price_dellin


if __name__ == '__main__':

    ltl_price = price(
        'Воронеж Труда 59',
        'Москва Волоколамское 39'
    )

    # Result: LTL price is 11070.0
    print('LTL price is', ltl_price)
