import pandas as pd
import numpy as np
from surprise import SVD, Dataset, Reader
import sqlite3
import os
import warnings
warnings.filterwarnings('ignore')

# Get absolute path to the database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database/database.db')

# Function to check if database exists
def check_database():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        print("Please run the setup script first: python setup_foodaware.py")
        return False
    return True

# Collaborative Filtering with SVD
def recommend_foods(user_id, n=5):
    """
    Recommends foods for a user based on collaborative filtering (SVD).
    
    Args:
        user_id (str): The user ID for whom to generate recommendations
        n (int): Number of recommendations to return
        
    Returns:
        DataFrame: A DataFrame containing food_id and score
    """
    try:
        # Check if database exists
        if not check_database():
            # Create dummy recommendations
            return pd.DataFrame({
                'food_id': [f'f{i}' for i in range(1, n+1)],
                'score': [0.5 for _ in range(n)]
            })
        
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        
        # Get orders data
        orders_df = pd.read_sql_query("SELECT user_id, food_id FROM orders", conn)
        
        # If rating column exists, use it, otherwise create implicit rating
        try:
            orders_df['rating'] = pd.read_sql_query("SELECT rating FROM orders", conn)
        except:
            orders_df['rating'] = 1  # Assign implicit rating
            
        # Get food items for output enrichment
        food_items_df = pd.read_sql_query("SELECT food_id, name, cuisine, category FROM food_items", conn)
        conn.close()
        
        # Check if we have data
        if orders_df.empty:
            print("⚠️ No orders data found in database")
            return pd.DataFrame(columns=['food_id', 'score'])
            
        # Check if user exists in orders
        if user_id not in orders_df['user_id'].unique():
            print(f"⚠️ User {user_id} not found in orders data")
            # Return random recommendations
            random_foods = food_items_df.sample(n=n)
            return pd.DataFrame({
                'food_id': random_foods['food_id'],
                'score': np.random.uniform(3, 5, size=n)
            })
        
        # Set up Surprise reader and dataset
        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(orders_df[['user_id', 'food_id', 'rating']], reader)
        trainset = data.build_full_trainset()
        
        # Train SVD model
        model = SVD()
        model.fit(trainset)
        
        # Get all food IDs
        food_ids = food_items_df['food_id'].unique()
        
        # Generate predictions
        predictions = []
        for food_id in food_ids:
            # Skip items the user has already ordered
            user_orders = orders_df[orders_df['user_id'] == user_id]['food_id']
            if food_id in user_orders.values:
                continue
                
            # Predict rating
            pred = model.predict(user_id, food_id)
            predictions.append((food_id, pred.est))
        
        # Sort by predicted score
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        # Return top N recommendations
        top_n = predictions[:n]
        recommendations_df = pd.DataFrame(top_n, columns=['food_id', 'score'])
        
        # Add food details
        recommendations_df = pd.merge(
            recommendations_df,
            food_items_df,
            on='food_id',
            how='left'
        )
        
        return recommendations_df
        
    except Exception as e:
        print(f"❌ Error in collaborative filtering: {str(e)}")
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['food_id', 'score', 'name', 'cuisine', 'category'])