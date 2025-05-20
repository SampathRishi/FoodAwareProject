import pandas as pd
import sqlite3
import os
import random

# Get absolute path to the database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database/database.db')

# Import recommendation models
from models.collaborative_filtering import recommend_foods as cf_recommend
from models.content_based_filtering import recommend_content_based as cb_recommend
from models.context_aware_filtering import recommend_context_aware as ca_recommend

# Function to check if database exists
def check_database():
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        print("Please run the setup script first: python setup_foodaware.py")
        return False
    return True

# Weight configuration
CF_WEIGHT = 0.4
CB_WEIGHT = 0.3
CA_WEIGHT = 0.3

# Hybrid Recommendation Logic
def hybrid_recommendation(user_id, weather, mood, n=5):
    """
    Generates hybrid recommendations combining collaborative, content-based, and context-aware approaches.
    
    Args:
        user_id (str): The user ID for whom to generate recommendations
        weather (str): Current weather condition
        mood (str): Current mood
        n (int): Number of recommendations to return
        
    Returns:
        list: A list of dictionaries containing hybrid-scored food recommendations
    """
    try:
        # Check if database exists
        if not check_database():
            # Create dummy recommendations
            return [
                {
                    'food_id': f'f{i}', 
                    'name': f'Food {i}', 
                    'cuisine': 'Unknown', 
                    'category': 'Unknown',
                    'score': 0.5
                } for i in range(1, n+1)
            ]
            
        # Get recommendations from each model
        try:
            cf_recs = cf_recommend(user_id, n * 2)
            print(f"✅ Got {len(cf_recs)} collaborative filtering recommendations")
        except Exception as e:
            print(f"⚠️ Error in collaborative filtering: {str(e)}")
            cf_recs = pd.DataFrame(columns=['food_id', 'score'])
            
        try:
            cb_recs = cb_recommend(user_id, weather, mood, n * 2)
            print(f"✅ Got {len(cb_recs)} content-based recommendations")
        except Exception as e:
            print(f"⚠️ Error in content-based filtering: {str(e)}")
            cb_recs = pd.DataFrame(columns=['food_id', 'name', 'cuisine', 'category', 'score'])
            
        try:
            ca_recs = ca_recommend(user_id, weather, mood, n * 2)
            ca_recs = pd.DataFrame(ca_recs)
            print(f"✅ Got {len(ca_recs)} context-aware recommendations")
        except Exception as e:
            print(f"⚠️ Error in context-aware filtering: {str(e)}")
            ca_recs = pd.DataFrame(columns=['food_id', 'name', 'cuisine', 'category'])
        
        # If any of the recommendation systems returned empty results, 
        # fetch food items directly from database
        if cf_recs.empty and cb_recs.empty and ca_recs.empty:
            print("⚠️ All recommendation systems failed, using fallback")
            conn = sqlite3.connect(DB_PATH)
            food_items_df = pd.read_sql_query("SELECT food_id, name, cuisine, category FROM food_items LIMIT ?", conn, params=(n,))
            conn.close()
            
            food_items_df['score'] = 0.5  # Default score
            return food_items_df.to_dict(orient='records')
        
        # Add weights to each recommendation set
        if not cf_recs.empty and 'score' in cf_recs.columns:
            cf_recs['score'] = cf_recs['score'] * CF_WEIGHT
        
        if not cb_recs.empty and 'score' in cb_recs.columns:
            cb_recs['score'] = cb_recs['score'] * CB_WEIGHT
        
        if not ca_recs.empty:
            # Add score column if it doesn't exist
            if 'score' not in ca_recs.columns:
                ca_recs['score'] = 1.0  # Default score
            ca_recs['score'] = ca_recs['score'] * CA_WEIGHT
        
        # Combine and group by food_id, summing the scores
        # First make sure all necessary columns exist
        for df in [cf_recs, cb_recs, ca_recs]:
            if not df.empty:
                for col in ['name', 'cuisine', 'category']:
                    if col not in df.columns:
                        # Connect to database to get missing info
                        conn = sqlite3.connect(DB_PATH)
                        food_details = pd.read_sql_query(
                            "SELECT food_id, name, cuisine, category FROM food_items", conn
                        )
                        conn.close()
                        
                        # Merge with recommendations
                        df = pd.merge(df, food_details, on='food_id', how='left')
                
                # Fill NaN values
                for col in ['name', 'cuisine', 'category']:
                    if col in df.columns:
                        df[col] = df[col].fillna("Unknown")
        
        # Concatenate all recommendation sources
        dfs_to_concat = []
        if not cf_recs.empty:
            dfs_to_concat.append(cf_recs)
        if not cb_recs.empty:
            dfs_to_concat.append(cb_recs)
        if not ca_recs.empty:
            dfs_to_concat.append(ca_recs)
            
        if not dfs_to_concat:
            # This should not happen as we have a fallback above
            print("⚠️ No recommendations to combine")
            return [
                {
                    'food_id': f'f{i}', 
                    'name': f'Food {i}', 
                    'cuisine': 'Unknown', 
                    'category': 'Unknown',
                    'score': 0.5
                } for i in range(1, n+1)
            ]
            
        combined_df = pd.concat(dfs_to_concat, ignore_index=True)
        
        # Group by food_id and aggregate
        combined_df = combined_df.groupby('food_id').agg({
            'score': 'sum',
            'name': 'first',
            'cuisine': 'first',
            'category': 'first'
        }).reset_index()
        
        # Sort by score and return top N
        combined_df = combined_df.sort_values(by='score', ascending=False).head(n)
        
        return combined_df.to_dict(orient='records')
        
    except Exception as e:
        print(f"❌ Error in hybrid recommendation: {str(e)}")
        # Return dummy recommendations
        return [
            {
                'food_id': f'f{i}', 
                'name': f'Food {i}', 
                'cuisine': 'Unknown', 
                'category': 'Unknown',
                'score': 0.5
            } for i in range(1, n+1)
        ]