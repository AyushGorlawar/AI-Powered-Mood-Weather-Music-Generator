# AI-Powered Mood & Weather-Based Music Recommendation System

### An AI-powered music recommendation system that suggests songs and Spotify playlists based on your mood and the weather


This project is an AI-driven Flask-based music recommendation system that suggests Spotify playlists based on your mood and the current weather. It leverages NLP to analyze mood from text input and fetches relevant playlists using Spotify's API.

## Features
- Detects mood from text input using NLP (TextBlob)
- Fetches weather details based on the user's city
- Suggests Spotify playlists based on mood and weather
- Uses Spotify OAuth authentication to access playlists

## Tech Stack
- **Backend**: Flask, Python
- **APIs**: OpenWeather API, Spotify API
- **NLP**: TextBlob
- **Authentication**: Spotify OAuth

## Installation
### 1. Clone the Repository
 
### 2. Create a Virtual Environment (Optional but Recommended)
```bash
    python -m venv venv
    venv\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
    pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root and add the following details:
```ini
SECRET_KEY=your_secret_key
WEATHER_API_KEY=your_openweather_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
```

> Replace the placeholders with your actual API keys and credentials.

## Running the Application
```bash
    python app.py
```
The Flask server will start at `http://127.0.0.1:5000/`.

## Usage
1. Open the application in your browser.
2. Log in with your Spotify account.
3. Enter your mood and city.
4. Get personalized Spotify playlists based on mood & weather.

## API Endpoints
### 1. **GET /**
   - Renders the homepage.

### 2. **POST /get_music**
   - **Input** (JSON):
     ```json
     {
       "city": "Mumbai",
       "mood": "I am feeling energetic today!"
     }
     ```
   - **Response** (JSON):
     ```json
     {
       "mood": "happy",
       "weather": "clear",
       "playlist": "Happy Beats + Clear Sky Vibes"
     }
     ```

### 3. **GET /login**
   - Redirects to Spotify authentication page.

### 4. **GET /callback**
   - Handles Spotify OAuth authentication.

## Troubleshooting
- If you face Spotify authentication issues, ensure your **redirect URI** in the Spotify developer dashboard matches the one in `.env`.
- If weather data isn't fetching, check your OpenWeather API key and city name spelling.
- For debugging, enable Flask logs with `app.run(debug=True)`.

## Contributing
Feel free to fork the repo, create a feature branch, and submit a pull request!

## License
Apache2.0 license

## Author
Ayush Gorlawar

