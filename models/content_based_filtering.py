import pandas as pd
import numpy as np
import sqlite3
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

# Content-Based Filtering
def recommend_content_based(user_id, weather, mood, n=5):
    """
    Recommends food items based on content similarity for a given user.
    
    Args:
        user_id (str): The user ID for whom to generate recommendations
        weather (str): Current weather condition
        mood (str): Current mood
        n (int): Number of recommendations to return
        
    Returns:
        DataFrame: A DataFrame with food items and their content-based scores
    """
    try:
        # Check if database exists
        if not check_database():
            # Create dummy recommendations
            return pd.DataFrame(columns=['food_id', 'name', 'cuisine', 'category', 'score'])
        
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        
        # Get food items
        food_items_df = pd.read_sql_query("SELECT * FROM food_items", conn)
        
        # Get user preferences
        users_df = pd.read_sql_query("SELECT * FROM users WHERE user_id = ?", conn, params=(user_id,))
        
        # Close connection
        conn.close()
        
        # Check if we have data
        if food_items_df.empty:
            print("⚠️ No food items found in database")
            return pd.DataFrame(columns=['food_id', 'name', 'cuisine', 'category', 'score'])
            
        # Check if user exists
        if users_df.empty:
            print(f"⚠️ User {user_id} not found in database")
            # Return random recommendations
            random_foods = food_items_df.sample(n=n)
            random_foods['score'] = np.random.uniform(0.5, 0.9, size=len(random_foods))
            return random_foods[['food_id', 'name', 'cuisine', 'category', 'score']]
        
        # Process cuisine preferences
        cuisine_prefs = users_df['cuisine_preferences'].values[0]
        if isinstance(cuisine_prefs, str):
            if '[' in cuisine_prefs:
                # Handle list stored as string
                try:
                    cuisine_prefs = eval(cuisine_prefs.replace("'", "\""))
                except:
                    cuisine_prefs = [cuisine_prefs]
            else:
                cuisine_prefs = [c.strip() for c in cuisine_prefs.split(',')]
        
        # Process dietary restrictions
        dietary = users_df['dietary_restrictions'].values[0]
        if isinstance(dietary, str):
            if '[' in dietary:
                try:
                    dietary = eval(dietary.replace("'", "\""))
                except:
                    dietary = [dietary]
            else:
                dietary = [d.strip() for d in dietary.split(',')]
        
        # Make sure tags and attributes are strings
        food_items_df['tags'] = food_items_df['tags'].fillna('').astype(str)
        food_items_df['attributes'] = food_items_df['attributes'].fillna('').astype(str)
        
        # Create combined features column
        food_items_df['combined_features'] = food_items_df.apply(
            lambda x: f"{x['cuisine']} {x['category']} {x['tags']} {x['attributes']}",
            axis=1
        )
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        
        try:
            # Transform food features
            tfidf_matrix = vectorizer.fit_transform(food_items_df['combined_features'])
            
            # Build query vector
            cuisine_str = ' '.join(cuisine_prefs) if isinstance(cuisine_prefs, list) else cuisine_prefs
            dietary_str = ' '.join(dietary) if isinstance(dietary, list) else dietary
            query = f"{cuisine_str} {dietary_str} {weather} {mood}"
            
            # Vectorize query
            query_vec = vectorizer.transform([query])
            
            # Calculate similarity
            cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            # Get top N indices
            indices = cosine_similarities.argsort()[-n:][::-1]
            
            # Get recommended foods
            recommended_foods = food_items_df.iloc[indices].copy()
            recommended_foods['score'] = cosine_similarities[indices]
            
            return recommended_foods[['food_id', 'name', 'cuisine', 'category', 'score']]
            
        except Exception as e:
            print(f"⚠️ Error in TF-IDF processing: {str(e)}")
            # Fallback to simple filtering
            matching_foods = food_items_df[food_items_df['cuisine'].isin(cuisine_prefs)].copy()
            
            if matching_foods.empty or len(matching_foods) < n:
                # Not enough matches, get random items
                matching_foods = food_items_df.sample(n=n)
            
            matching_foods['score'] = np.random.uniform(0.5, 0.9, size=len(matching_foods))
            matching_foods = matching_foods.sort_values('score', ascending=False).head(n)
            
            return matching_foods[['food_id', 'name', 'cuisine', 'category', 'score']]
        
    except Exception as e:
        print(f"❌ Error in content-based filtering: {str(e)}")
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['food_id', 'name', 'cuisine', 'category', 'score'])