import requests

def check_price(symbol):
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={symbol}"
    headers = {
        "Accepts": "application/json",
        "X-CMC_Pro_API_Key": "8754985f-a54e-490a-8665-5840d4cb6556"
    }
    response = requests.get(url, headers=headers).json()
    price = response["data"][symbol]["quote"]["USD"]["price"]
    return price

# symbols = ["BTC", "ETH", "XRP", "BNB"]
# for symbol in symbols:
#     price = check_price(symbol)
#     print(f"The price of {symbol} is ${price:.2f}")


while True:
    symbol = input("Please write symbol>> ").upper()
    print(check_price(symbol=symbol))