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

async def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
	cursor.execute('INSERT INTO users (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)', (user_id, user_name, user_surname, username))
	conn.commit()
