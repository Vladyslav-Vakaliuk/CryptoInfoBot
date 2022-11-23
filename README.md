A Telegram Bot with cryptocurrency price and some other cool features.
You can check the price of a cryptocurrency in real time

https://t.me/crazycryptoinfobot

# How to use 
1. Clone this repository
```
git clone https://github.com/Vladyslav-Vakaliuk/CryptoInfoBot.git
```
2. Create a `config.py` file and add your tokens there, you must to add telegram bot token and etherscan API token 
```
BOT_TOKEN = 'Your Token' 
ETHERSCAN_TOKEN = 'Your Token' 
``` 
3. Install all requirements
```
pip install pyTelegramBotAPI 
pip install -U pycoingecko
pip install ethereum-gasprice
```
4)To run this bot use: 
```
python bot.py
```
