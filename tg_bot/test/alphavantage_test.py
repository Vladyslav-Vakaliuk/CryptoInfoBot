import requests

def check_price(symbol):
    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={symbol}&to_currency=USD&apikey=BO295VJFICM5LXW8"
    response = requests.get(url).json()
    return response

# symbols = ["BTC"]
# for symbol in symbols:
#     price = check_price(symbol)
#     print(f"The price of {symbol} is ${price:.2f}")


# price = response["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
# symbol = response["Realtime Currency Exchange Rate"]["1. From_Currency Code"]
# name = ["Realtime Currency Exchange Rate"]["2. From_Currency Name"]


print(check_price("BTC"))

