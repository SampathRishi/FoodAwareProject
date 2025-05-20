import os
import pandas as pd
import sqlite3

# Get absolute path to the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '../data')
DB_DIR = os.path.join(BASE_DIR, '../database')
DB_PATH = os.path.join(DB_DIR, 'database.db')

# Ensure the database directory exists
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def load_csv(filename):
    """Load CSV data from the data directory."""
    path = os.path.join(DATA_DIR, f'{filename}.csv')
    if os.path.exists(path):
        print(f"📌 Loading {filename}.csv...")
        df = pd.read_csv(path)
        print(f"✅ Loaded {len(df)} records from {filename}.csv.")
        print(f"📌 DataFrame Preview:\n{df.head()}\n")
        return df
    else:
        print(f"❌ {filename}.csv not found.")
        return pd.DataFrame()

def save_to_database(df, table_name, conn):
    """Save DataFrame to SQLite database."""
    print(f"📌 Saving {table_name} to database...")
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    print(f"✅ {table_name} table updated with {len(df)} records.")

def verify_database(conn):
    """Verify data loaded into the database."""
    print(f"\n📌 Verifying database contents...")
    tables = ['users', 'food_items', 'orders']
    for table in tables:
        print(f"\n📌 Preview of {table} table:")
        query = f"SELECT * FROM {table} LIMIT 5"
        df = pd.read_sql_query(query, conn)
        print(df)

def main():
    print("📌 Loading CSV files...")
    
    # Load CSVs
    users_df = load_csv('users')
    food_items_df = load_csv('food_items')
    orders_df = load_csv('orders')
    
    # Verify all data is loaded
    if users_df.empty or food_items_df.empty or orders_df.empty:
        print("❌ Missing data. Please generate synthetic data and try again.")
        return

    print("📌 Saving to database...")
    
    # Connect to SQLite database
    with sqlite3.connect(DB_PATH) as conn:
        # Save DataFrames to the database
        save_to_database(users_df, 'users', conn)
        save_to_database(food_items_df, 'food_items', conn)
        save_to_database(orders_df, 'orders', conn)

        # Verify the contents
        verify_database(conn)
        
    print("\n✅ Data loaded into the database!")

if __name__ == '__main__':
    main()
