import os
import sqlite3

# Ensure the folder exists
os.makedirs('../database', exist_ok=True)

# Database schema
SCHEMA_SQL = '''
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    age INTEGER,
    gender TEXT,
    cuisine_preferences TEXT,
    dietary_restrictions TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS food_items (
    food_id TEXT PRIMARY KEY,
    name TEXT,
    cuisine TEXT,
    category TEXT,
    price REAL,
    tags TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    food_id TEXT,
    timestamp TEXT,
    mood TEXT,
    weather TEXT,
    location TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(food_id) REFERENCES food_items(food_id)
);
'''

# Initialize the database
def setup_database():
    conn = sqlite3.connect('../database/database.db')
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print("Database setup complete!")

setup_database()
