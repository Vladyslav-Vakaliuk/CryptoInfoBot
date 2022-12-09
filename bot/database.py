import json
import pandas as pd
import sqlite3
from sqlite3 import Error



def db_connect():
    try:
        global conn, cursor
        conn = sqlite3.connect('database.db', check_same_thread=False)
        cursor = conn.cursor()
    except Error as e:
        print(f"The error '{e}' occurred")

    conn.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    user_id INTEGER UNIQUE NOT NULL,
                    user_name TEXT INTEGER NOT NULL,
                    user_surname TEXT,
                    username STRING TEXT,
                    language TEXT
                );  """)

def create_coins_table():
    # # Open JSON data
    with open("bot/source/coins.json", "rb") as f:
        data = json.load(f)
    try:
        # Create A DataFrame From the JSON Data
        df = pd.DataFrame(data)
        df.to_sql("coins", conn)
    except:
        pass

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, language: str):
	cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username, language) VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_surname, username, language))
	conn.commit()

def find_id(symbol: str):
    cursor.execute('SELECT id, name FROM coins WHERE symbol = ?', (symbol,))
    conn.commit()
    global coin
    coin = cursor.fetchone()[0]

def find_name(symbol: str):
    cursor.execute('SELECT name FROM coins WHERE symbol = ?', (symbol,))
    conn.commit()
    global name
    name = cursor.fetchone()[0]

