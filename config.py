from decouple import config

# bot settings
BOT_TOKEN = config("BOT_TOKEN")
ADMINS = config("ADMINS")

# psql settings 
DB_USER = config("DB_USER")
PG_PASSWORD = config("PG_PASSWORD")
DB_NAME = config("DB_NAME")
DB_HOST = config("DB_HOST")
DB_PORT = config("PORT")

# misc 
CMC_TOKEN = config("CMC_API_TOKEN")
ETHERSCAN_TOKEN = config("ETHERSCAN_TOKEN")
