#!/usr/bin/env python3
"""
FOODAWARE Setup Script
This script sets up the complete FOODAWARE application by:
1. Creating necessary directories
2. Initializing the database
3. Generating synthetic data
4. Loading data into the database
"""

import os
import sys
import subprocess
import sqlite3
import pandas as pd
import time

print("🚀 FOODAWARE Setup - Starting...")

# Create necessary directories
directories = [
    'data',
    'database',
    'models',
    'static/css',
    'static/js',
    'static/images'
]

print("\n📂 Creating directory structure...")
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"  ✅ Created: {directory}")

# Create models/__init__.py if it doesn't exist
init_path = 'models/__init__.py'
if not os.path.exists(init_path):
    with open(init_path, 'w') as f:
        f.write("# Models package for FOODAWARE\n")
    print(f"  ✅ Created: {init_path}")

# Set up database
print("\n🗄️ Setting up database...")

# Database schema with additional ensures rating column is present
SCHEMA_SQL = '''
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT,
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
    tags TEXT,
    attributes TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    user_id TEXT,
    food_id TEXT,
    timestamp TEXT,
    mood TEXT,
    weather TEXT,
    location TEXT,
    rating INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(food_id) REFERENCES food_items(food_id)
);
'''

def setup_database():
    db_path = 'database/database.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print(f"  ✅ Database schema created at {db_path}")

setup_database()

# Check if we already have data files
print("\n📊 Checking for existing data...")
users_exists = os.path.exists('data/users.csv')
food_items_exists = os.path.exists('data/food_items.csv')
orders_exists = os.path.exists('data/orders.csv')

# If data files don't exist, we need to generate them
if not (users_exists and food_items_exists and orders_exists):
    print("  ⚠️ Data files not found, creating sample data...")
    
    # Create sample data
    print("  📝 Generating sample data...")
    
    # Sample users
    users_data = [
        {
            'user_id': 'u1',
            'name': 'John Smith',
            'age': 35,
            'gender': 'Male',
            'cuisine_preferences': "['Italian', 'Mexican', 'American']",
            'dietary_restrictions': "['Gluten-Free']",
            'location': 'New York'
        },
        {
            'user_id': 'u2',
            'name': 'Maria Garcia',
            'age': 28,
            'gender': 'Female',
            'cuisine_preferences': "['Japanese', 'Thai', 'Indian']",
            'dietary_restrictions': "['Vegetarian']",
            'location': 'Los Angeles'
        },
        {
            'user_id': 'u3',
            'name': 'David Kim',
            'age': 42,
            'gender': 'Male',
            'cuisine_preferences': "['Chinese', 'Korean', 'Japanese']",
            'dietary_restrictions': "['None']",
            'location': 'Chicago'
        },
        {
            'user_id': 'u4',
            'name': 'Sarah Johnson',
            'age': 31,
            'gender': 'Female',
            'cuisine_preferences': "['Italian', 'French', 'American']",
            'dietary_restrictions': "['Keto', 'Dairy-Free']",
            'location': 'Boston'
        },
        {
            'user_id': 'u5',
            'name': 'Michael Brown',
            'age': 25,
            'gender': 'Male',
            'cuisine_preferences': "['Mexican', 'American', 'Thai']",
            'dietary_restrictions': "['Vegan']",
            'location': 'Miami'
        }
    ]
    
    # Sample food items
    food_items_data = [
        {
            'food_id': 'f1',
            'name': 'Margherita Pizza',
            'cuisine': 'Italian',
            'category': 'Main Course',
            'price': 12.99,
            'tags': 'Vegetarian,Classic',
            'attributes': 'Savory'
        },
        {
            'food_id': 'f2',
            'name': 'Spicy Tuna Roll',
            'cuisine': 'Japanese',
            'category': 'Appetizer',
            'price': 8.99,
            'tags': 'Seafood,Spicy',
            'attributes': 'Spicy'
        },
        {
            'food_id': 'f3',
            'name': 'Beef Tacos',
            'cuisine': 'Mexican',
            'category': 'Main Course',
            'price': 10.99,
            'tags': 'Meat,Spicy',
            'attributes': 'Savory'
        },
        {
            'food_id': 'f4',
            'name': 'Pad Thai',
            'cuisine': 'Thai',
            'category': 'Main Course',
            'price': 11.99,
            'tags': 'Noodles,Peanuts',
            'attributes': 'Savory'
        },
        {
            'food_id': 'f5',
            'name': 'Chicken Tikka Masala',
            'cuisine': 'Indian',
            'category': 'Main Course',
            'price': 13.99,
            'tags': 'Spicy,Curry',
            'attributes': 'Spicy'
        },
        {
            'food_id': 'f6',
            'name': 'Caesar Salad',
            'cuisine': 'American',
            'category': 'Appetizer',
            'price': 7.99,
            'tags': 'Healthy,Salad',
            'attributes': 'Fresh'
        },
        {
            'food_id': 'f7',
            'name': 'Chocolate Cake',
            'cuisine': 'American',
            'category': 'Dessert',
            'price': 6.99,
            'tags': 'Sweet,Dessert',
            'attributes': 'Sweet'
        },
        {
            'food_id': 'f8',
            'name': 'Beef Burger',
            'cuisine': 'American',
            'category': 'Main Course',
            'price': 9.99,
            'tags': 'Meat,Fast Food',
            'attributes': 'Savory'
        },
        {
            'food_id': 'f9',
            'name': 'Green Curry',
            'cuisine': 'Thai',
            'category': 'Main Course',
            'price': 12.99,
            'tags': 'Spicy,Coconut',
            'attributes': 'Spicy'
        },
        {
            'food_id': 'f10',
            'name': 'Miso Soup',
            'cuisine': 'Japanese',
            'category': 'Appetizer',
            'price': 3.99,
            'tags': 'Soup,Umami',
            'attributes': 'Savory'
        },
        {
            'food_id': 'f11',
            'name': 'Tiramisu',
            'cuisine': 'Italian',
            'category': 'Dessert',
            'price': 7.99,
            'tags': 'Sweet,Coffee',
            'attributes': 'Sweet'
        },
        {
            'food_id': 'f12',
            'name': 'Mango Lassi',
            'cuisine': 'Indian',
            'category': 'Beverage',
            'price': 4.99,
            'tags': 'Sweet,Yogurt',
            'attributes': 'Sweet'
        },
        {
            'food_id': 'f13',
            'name': 'Guacamole',
            'cuisine': 'Mexican',
            'category': 'Appetizer',
            'price': 5.99,
            'tags': 'Vegan,Healthy',
            'attributes': 'Fresh'
        },
        {
            'food_id': 'f14',
            'name': 'Spaghetti Carbonara',
            'cuisine': 'Italian',
            'category': 'Main Course',
            'price': 13.99,
            'tags': 'Pasta,Creamy',
            'attributes': 'Savory'
        },
        {
            'food_id': 'f15',
            'name': 'Chicken Wings',
            'cuisine': 'American',
            'category': 'Appetizer',
            'price': 8.99,
            'tags': 'Spicy,Meat',
            'attributes': 'Spicy'
        }
    ]
    
    # Sample orders with explicit rating column
    import random
    from datetime import datetime, timedelta
    
    orders_data = []
    for i in range(1, 101):  # Generate 100 sample orders
        user_id = f'u{random.randint(1, 5)}'
        food_id = f'f{random.randint(1, 15)}'
        
        # Random date in the last year
        days_ago = random.randint(0, 365)
        order_date = datetime.now() - timedelta(days=days_ago)
        
        # Get user location
        user_location = next((user['location'] for user in users_data if user['user_id'] == user_id), 'Unknown')
        
        orders_data.append({
            'order_id': f'o{i}',
            'user_id': user_id,
            'food_id': food_id,
            'timestamp': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'mood': random.choice(['Happy', 'Sad', 'Stressed', 'Relaxed', 'Adventurous']),
            'weather': random.choice(['Sunny', 'Rainy', 'Cloudy', 'Snowy', 'Windy']),
            'location': user_location,
            'rating': random.randint(1, 5)  # Explicit rating between 1-5
        })
    
    # Save to CSV files
    users_df = pd.DataFrame(users_data)
    food_items_df = pd.DataFrame(food_items_data)
    orders_df = pd.DataFrame(orders_data)
    
    users_df.to_csv('data/users.csv', index=False)
    food_items_df.to_csv('data/food_items.csv', index=False)
    orders_df.to_csv('data/orders.csv', index=False)
    
    print("  ✅ Sample data created")
else:
    print("  ✅ Data files found")

# Load data into the database
print("\n📥 Loading data into database...")

def load_data_into_db():
    users_df = pd.read_csv('data/users.csv')
    food_items_df = pd.read_csv('data/food_items.csv')
    orders_df = pd.read_csv('data/orders.csv')
    
    conn = sqlite3.connect('database/database.db')
    
    users_df.to_sql('users', conn, if_exists='replace', index=False)
    food_items_df.to_sql('food_items', conn, if_exists='replace', index=False)
    orders_df.to_sql('orders', conn, if_exists='replace', index=False)
    
    conn.close()
    print("  ✅ Data loaded into database")

load_data_into_db()

# Verify database tables
print("\n🔍 Verifying database tables...")
conn = sqlite3.connect('database/database.db')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"  📋 Tables in database: {[table[0] for table in tables]}")

# Verify each table has data
for table in [table[0] for table in tables]:
    if table.startswith('sqlite'):
        continue
    cursor.execute(f"SELECT COUNT(*) FROM {table};")
    count = cursor.fetchone()[0]
    print(f"  ✅ Table '{table}' has {count} records")

conn.close()

# Create example .env file if it doesn't exist
env_path = '.env'
if not os.path.exists(env_path):
    with open(env_path, 'w') as f:
        f.write("""# API Keys
OPENAI_API_KEY=your_openai_api_key_here
WEATHER_API_KEY=your_weather_api_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
""")
    print("\n📝 Created .env file template - please update with your API keys")

print("\n🎉 FOODAWARE Setup Complete! You can now run the application with:")
print("   streamlit run app.py")
