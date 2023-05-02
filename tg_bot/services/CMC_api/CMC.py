import requests

from decouple import config

CMC_TOKEN = config("CMC_API_TOKEN")

class CMC():
    
    def check_price(symbol):
        url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {
            "Accepts": "application/json",
            "X-CMC_Pro_API_Key": CMC_TOKEN
        }
        params = {
            'symbol' : symbol
        }
        response = requests.get(url, headers=headers, params=params).json()
        return response

    def convert_currency(amount, symbol):
        url = f"https://pro-api.coinmarketcap.com/v2/tools/price-conversion"
        headers = {
            "Accepts": "application/json",
            "X-CMC_Pro_API_Key": CMC_TOKEN
        }
        params = {
            'amount' : amount,
            'symbol' : symbol

        }
        response = requests.get(url, headers=headers, params=params).json()
        return response


