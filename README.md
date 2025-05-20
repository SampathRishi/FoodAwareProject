# FOODAWARE - AI Food Recommendation System

FOODAWARE is an intelligent food recommendation system that suggests food items based on user preferences, current weather conditions, and detected mood.

## Demo Videos

### Main Application Demo
[Download App Demo Video](app.mov)

### Analytics Dashboard Demo
[Download Analytics Demo Video](analytics.mov)

## Features

- **User Profile Management**: Select from existing user profiles with their preferences
- **Weather Integration**: Automatically fetches current weather for the user's location
- **Mood Detection**: Uses OpenAI to analyze chat messages and detect user's mood
- **Multiple Recommendation Algorithms**:
  - Collaborative Filtering: Based on similar users' preferences
  - Content-Based Filtering: Based on item features and user preferences
  - Context-Aware Filtering: Based on current weather and mood
  - Hybrid Recommendation: Combines all approaches for optimal suggestions
- **Nearby Restaurant Search**: Find restaurants serving recommended cuisines

## Setup Instructions

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.template` to `.env` and fill in your API keys:
   ```
   cp .env.template .env
   ```
4. Run the data generation script to create synthetic data (if not already done):
   ```
   python generate_synthetic_data.py
   ```
5. Set up the database:
   ```
   python setup_database.py
   python load_data.py
   ```
6. Launch the Streamlit app:
   ```
   streamlit run app.py
   ```

## Project Structure

- `/data`: Contains CSV files with user, food item, and order data
- `/database`: SQLite database for the application
- `/models`: Recommendation algorithm implementations
- `/static`: CSS, JavaScript, and image assets
- `app.py`: Main Streamlit application
- `*.py`: Various utility scripts for data generation, API access, etc.

## API Keys Required

- **OpenAI API Key**: For mood detection from conversation
- **Weather API Key**: From OpenWeatherMap to get current weather conditions
- **Google Maps API Key**: For finding nearby restaurants (optional)

## Technologies Used

- **Streamlit**: For building the web application interface
- **Pandas & NumPy**: For data manipulation
- **Scikit-learn**: For machine learning models
- **SQLite**: For database storage
- **OpenAI API**: For mood detection
- **Various external APIs**: For weather and location data

## License

This project is for educational purposes only.