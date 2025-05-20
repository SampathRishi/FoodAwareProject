import openai
import os
from dotenv import load_dotenv

load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_user_name():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You generate realistic first and last names."},
                {"role": "user", "content": "Give a realistic human name."}
            ],
            max_tokens=10,
            temperature=0.7
        )
        name = response['choices'][0]['message']['content'].strip()
        return name if name else "Alex Smith"
    except Exception as e:
        print(f"[Name Generation Error]: {e}")
        return "Alex Smith"

CUISINE_STYLES = {
    'Italian': "Italian",
    'Chinese': "Chinese",
    'Indian': "Indian",
    'Mexican': "Mexican",
    'Japanese': "Japanese",
    'Thai': "Thai",
    'American': "American"
}

def generate_food_name(cuisine):
    prompt = f"Suggest a realistic and creative {cuisine} dish name for a food delivery app."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chef generating fun dish names."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=20,
            temperature=0.8,
            n=1
        )
        name = response['choices'][0]['message']['content'].strip()
        return name if name else f"{cuisine} Dish"
    except Exception as e:
        print(f"[Name Generation Error]: {e}")
        return f"{cuisine} Dish"
