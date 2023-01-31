from decouple import config

# bot settings
BOT_TOKEN = config("BOT_TOKEN")
ADMINS = config("ADMINS")

# psql settings 
BD_USER = config("DB_USER")
PG_PASSWORD = config("PG_PASSWORD")
BD_NAME = config("DB_NAME")
BD_HOST = config("DB_HOST")
PORT = config("PORT")

# misc 
ETHERSCAN_TOKEN = config("ETHERSCAN_TOKEN")