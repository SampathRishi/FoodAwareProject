import pandas as pd
import sqlite3
import os
import random

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

# Context-Based Rules
WEATHER_RULES = {
    'Sunny': ['Salad', 'Appetizer', 'Cold Drinks', 'Dessert'],
    'Rainy': ['Soup', 'Hot Coffee', 'Main Course', 'Stew'],
    'Snowy': ['Hot Chocolate', 'Stew', 'Main Course', 'Soup'],
    'Cloudy': ['Tea', 'Appetizer', 'Sandwich', 'Dessert'],
    'Windy': ['Main Course', 'Appetizer', 'Wrap', 'Soup']
}

MOOD_RULES = {
    'Happy': ['Dessert', 'Appetizer', 'Salad', 'Beverage'],
    'Sad': ['Dessert', 'Main Course', 'Pasta', 'Comfort Food'],
    'Stressed': ['Main Course', 'Appetizer', 'Comfort Food', 'Beverage'],
    'Relaxed': ['Soup', 'Tea', 'Appetizer', 'Salad'],
    'Adventurous': ['Spicy', 'Main Course', 'Curry', 'Exotic']
}

# Context-Aware Filtering Logic
def recommend_context_aware(user_id, weather, mood, n=5):
    """
    Recommends food items based on contextual factors like weather and mood.
    
    Args:
        user_id (str): The user ID for whom to generate recommendations
        weather (str): Current weather condition
        mood (str): Current mood
        n (int): Number of recommendations to return
        
    Returns:
        list: A list of dictionaries containing food recommendations
    """
    try:
        # Check if database exists
        if not check_database():
            # Create dummy recommendations
            return [{'food_id': f'f{i}', 'name': f'Food {i}', 'cuisine': 'Unknown', 'category': 'Unknown'} for i in range(1, n+1)]
        
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        
        # Get food items
        food_items_df = pd.read_sql_query("SELECT * FROM food_items", conn)
        
        # Close connection
        conn.close()
        
        # Check if we have data
        if food_items_df.empty:
            print("⚠️ No food items found in database")
            return [{'food_id': f'f{i}', 'name': f'Food {i}', 'cuisine': 'Unknown', 'category': 'Unknown'} for i in range(1, n+1)]
        
        # Get contextual preferences
        weather_categories = WEATHER_RULES.get(weather, ['Main Course'])
        mood_categories = MOOD_RULES.get(mood, ['Main Course'])
        
        # Convert tags column to list if it's stored as string
        def process_tags(tags):
            if pd.isna(tags):
                return []
            if isinstance(tags, str):
                if tags.startswith('['):
                    try:
                        return eval(tags)
                    except:
                        pass
                return [tag.strip() for tag in tags.split(',')]
            return []
        
        # Apply tags processing if needed
        if 'tags' in food_items_df.columns and not food_items_df['tags'].empty:
            food_items_df['tags_list'] = food_items_df['tags'].apply(process_tags)
        else:
            food_items_df['tags_list'] = [[]] * len(food_items_df)
        
        # Score each food item based on contextual relevance
        scores = []
        
        for _, food in food_items_df.iterrows():
            score = 0
            
            # Check category match with weather
            if food['category'] in weather_categories:
                score += 1
                
            # Check category match with mood
            if food['category'] in mood_categories:
                score += 1
            
            # Check tags match with mood
            food_tags = food['tags_list'] if isinstance(food['tags_list'], list) else []
            if any(tag in str(food_tags) for tag in mood_categories):
                score += 0.5
                
            scores.append(score)
        
        food_items_df['context_score'] = scores
        
        # Filter items with some relevance
        relevant_items = food_items_df[food_items_df['context_score'] > 0].copy()
        
        # If not enough relevant items, add random items
        if len(relevant_items) < n:
            needed = n - len(relevant_items)
            random_items = food_items_df[~food_items_df['food_id'].isin(relevant_items['food_id'])]
            
            if len(random_items) >= needed:
                random_items = random_items.sample(n=needed)
            
            random_items['context_score'] = 0.1  # Low but non-zero score
            relevant_items = pd.concat([relevant_items, random_items])
        
        # Sort by score and select top n
        relevant_items = relevant_items.sort_values('context_score', ascending=False).head(n)
        
        # Convert to dictionary records for output
        return relevant_items[['food_id', 'name', 'cuisine', 'category']].to_dict(orient='records')
    
    except Exception as e:
        print(f"❌ Error in context-aware filtering: {str(e)}")
        # Return dummy recommendations
        return [{'food_id': f'f{i}', 'name': f'Food {i}', 'cuisine': 'Unknown', 'category': 'Unknown'} for i in range(1, n+1)]