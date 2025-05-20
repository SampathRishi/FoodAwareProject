import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
from generate_names import generate_user_name, generate_food_name

fake = Faker()

# Constants
NUM_USERS = 20
NUM_FOOD_ITEMS = 100
NUM_ORDERS = 5000
CUISINES = ['Italian', 'Chinese', 'Indian', 'Mexican', 'Japanese', 'Thai', 'American']
CUISINE_DISHES = {
    'Italian': ['Spaghetti Carbonara', 'Margherita Pizza', 'Lasagna', 'Risotto', 'Penne Arrabbiata'],
    'Chinese': ['Kung Pao Chicken', 'Sweet and Sour Pork', 'Dumplings', 'Mapo Tofu', 'Chow Mein'],
    'Indian': ['Butter Chicken', 'Palak Paneer', 'Biryani', 'Chole Bhature', 'Tandoori Roti'],
    'Mexican': ['Beef Tacos', 'Burrito Bowl', 'Quesadillas', 'Guacamole', 'Chicken Enchiladas'],
    'Japanese': ['Sushi Roll', 'Ramen', 'Tempura', 'Tonkatsu', 'Yakitori'],
    'Thai': ['Pad Thai', 'Green Curry', 'Tom Yum Soup', 'Thai Basil Chicken', 'Massaman Curry'],
    'American': ['Cheeseburger', 'Mac and Cheese', 'BBQ Ribs', 'Chicken Wings', 'Cobb Salad']
}
CATEGORIES = ['Breakfast', 'Lunch', 'Dinner', 'Appetizer', 'Main Course', 'Dessert']
MOODS = ['Happy', 'Sad', 'Stressed', 'Relaxed', 'Adventurous']
WEATHER = ['Sunny', 'Rainy', 'Snowy', 'Cloudy', 'Windy']
DIETARY_TAGS = ['Vegan', 'Vegetarian', 'Gluten-Free', 'Keto', 'Halal', 'Kosher']

# Generate Synthetic Users
def generate_users(num_users):
    users = []
    for _ in range(num_users):
        user = {
            'user_id': fake.uuid4(),
            'name': generate_user_name(),
            'age': random.randint(18, 65),
            'gender': random.choice(['Male', 'Female']),
            'cuisine_preferences': random.sample(CUISINES, k=3),
            'dietary_restrictions': random.sample(DIETARY_TAGS, k=2),
            'location': fake.city()
        }
        users.append(user)
    return pd.DataFrame(users)

# Generate Synthetic Food Items
def generate_food_items(num_items):
    food_items = []
    for _ in range(num_items):
        cuisine = random.choice(CUISINES)
        item = {
            'food_id': fake.uuid4(),
            'name': generate_food_name(cuisine),  # ✅ Pass cuisine
            'cuisine': cuisine,
            'category': random.choice(CATEGORIES),
            'price': round(random.uniform(5, 30), 2),
            'tags': random.sample(DIETARY_TAGS, k=2),
            'attributes': random.choice(['Spicy', 'Sweet', 'Savory', 'Tangy'])
        }
        food_items.append(item)
    return pd.DataFrame(food_items)

# Generate Synthetic Orders with Ratings
def generate_orders(num_orders, users, food_items):
    orders = []
    for _ in range(num_orders):
        user = users.sample(1).iloc[0]
        food_item = food_items.sample(1).iloc[0]
        order = {
            'order_id': fake.uuid4(),
            'user_id': user['user_id'],
            'food_id': food_item['food_id'],
            'timestamp': fake.date_time_between(start_date='-2y', end_date='now'),
            'mood': random.choice(MOODS),
            'weather': random.choice(WEATHER),
            'location': user['location'],
            'rating': random.randint(1, 5)  # Explicit rating
        }
        orders.append(order)
    return pd.DataFrame(orders)

# Main Generation
users_df = generate_users(NUM_USERS)
food_items_df = generate_food_items(NUM_FOOD_ITEMS)
orders_df = generate_orders(NUM_ORDERS, users_df, food_items_df)

# Save to CSV
users_df.to_csv('data/users.csv', index=False)
food_items_df.to_csv('data/food_items.csv', index=False)
orders_df.to_csv('data/orders.csv', index=False)

print("✅ Synthetic Data Generation Completed with 'rating' column in orders.csv!")
