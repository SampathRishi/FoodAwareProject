import openai
import os
from dotenv import load_dotenv

load_dotenv()
# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def detect_mood(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mood detection assistant. Just respond with the mood."},
                {"role": "user", "content": f"How am I feeling? {text}"}
            ],
            max_tokens=200,
            temperature=0.7
        )
        mood = response['choices'][0]['message']['content'].strip()
        return mood
    except Exception:
        return "Neutral"
