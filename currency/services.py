import requests
from django.conf import settings

def get_currency_conversion(from_currency, to_currency, amount):
    url = "https://currency-converter5.p.rapidapi.com/currency/convert"

    querystring = {
        "format": "json",
        "from": from_currency,
        "to": to_currency,
        "amount": str(amount)
    }

    headers = {
        "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
        "X-RapidAPI-Host": "currency-converter5.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        return data['rates'][to_currency]['rate_for_amount']
    else:
        return None
