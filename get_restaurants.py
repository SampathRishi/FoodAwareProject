import requests
import os

API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

def get_nearby_restaurants(location, food_type):
    try:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=1500&type=restaurant&keyword={food_type}&key={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        restaurants = []
        for place in data.get('results', []):
            restaurants.append({
                "name": place.get('name'),
                "address": place.get('vicinity'),
                "rating": place.get('rating')
            })
        return restaurants
    except Exception as e:
        return []
