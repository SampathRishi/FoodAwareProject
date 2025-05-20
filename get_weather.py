import requests
import os
from dotenv import load_dotenv

load_dotenv()
# Set OpenAI API key
API_KEY = os.getenv('WEATHER_API_KEY')

def get_weather(city):
    try:
        if not API_KEY:
            raise ValueError("WEATHER_API_KEY is not set.")

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            print(f"[Weather API Error]: {data}")
            return "Unknown", "N/A"

        weather = data['weather'][0]['main']           # e.g., "Rain"
        temp = round(data['main']['temp'], 1)          # e.g., 19.3°C
        return weather, temp

    except Exception as e:
        print(f"[Weather API Exception]: {e}")
        return "Unknown", "N/A"
