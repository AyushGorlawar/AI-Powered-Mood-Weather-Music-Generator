from flask import Flask, request, jsonify, redirect, render_template, session, url_for
import requests
from textblob import TextBlob
import random
import os
from dotenv import load_dotenv
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth

 
app = Flask(__name__)
 
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret_key")


# Load environment variables
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:5000/callback"

# Spotify OAuth
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="playlist-read-private"
)
# Enable debugging logs
logging.basicConfig(level=logging.DEBUG)
@app.route("/")
def index():
    return render_template("index.html")

 
def get_weather(city):
    if not city:
        return None
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("weather"):
        return response["weather"][0]["main"].lower()
    return None

def detect_mood(text):
    if not text:
        return "neutral"
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.3:
        return "happy"
    elif polarity < -0.3:
        return "sad"
    else:
        return "relaxed"
 
def get_spotify_playlist(mood, weather):
    token_info = session.get("token_info")

    if not token_info:
        print("⚠️ No Spotify Token Found. Redirecting to Login...")
        return redirect(url_for("login"))

    # ⚡ Refresh token if expired
    if sp_oauth.is_token_expired(token_info):
        print("🔄 Token Expired. Refreshing...")
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
        session["token_info"] = token_info

    try:
        sp = spotipy.Spotify(auth=token_info["access_token"])

        # Get Playlists
        mood_playlists = sp.search(q=f"{mood} music", type="playlist", limit=3)
        weather_playlists = sp.search(q=f"{weather} vibes", type="playlist", limit=3)

        mood_playlist_name = mood_playlists["playlists"]["items"][0]["name"] if mood_playlists["playlists"]["items"] else "Default Mood Playlist"
        weather_playlist_name = weather_playlists["playlists"]["items"][0]["name"] if weather_playlists["playlists"]["items"] else "Default Weather Playlist"

        return f"{mood_playlist_name} + {weather_playlist_name}"
    except Exception as e:
        print("❌ Spotify Error:", str(e))
        return "Error fetching Spotify playlists"
    
    token_info = session.get("token_info")
    if not token_info:
        return redirect(url_for("login")) 
    sp = spotipy.Spotify(auth=token_info["access_token"])

    
    mood_playlists = sp.search(q=f"{mood} music", type="playlist", limit=3)
    mood_playlist_name = (
        mood_playlists["playlists"]["items"][0]["name"]
        if mood_playlists["playlists"]["items"]
        else "Default Mood Playlist"
    )

 
    weather_playlists = sp.search(q=f"{weather} vibes", type="playlist", limit=3)
    weather_playlist_name = (
        weather_playlists["playlists"]["items"][0]["name"]
        if weather_playlists["playlists"]["items"]
        else "Default Weather Playlist"
    )

    return f"{mood_playlist_name} + {weather_playlist_name}"


@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    try:
        session.clear()
        code = request.args.get("code")
        token_info = sp_oauth.get_access_token(code)

        if not token_info:
            return "⚠️ Failed to get token", 400

        # ✅ Only Clear Session if Token is Invalid
        if "access_token" not in token_info:
            print("❌ Error getting access token.")
            return "Error logging in with Spotify", 400

        # Save Token
        session["token_info"] = token_info
        print("✅ Token Saved:", token_info)

        return redirect(url_for("home"))

    except Exception as e:
        print("❌ Callback Error:", str(e))
        return "Internal Server Error", 500
 

@app.route("/get_music", methods=["POST"])
def get_music():
    try:
        data = request.json
        print("📩 Received Data:", data)

        city = data.get("city")
        mood_input = data.get("mood")

        if not city:
            return jsonify({"error": "City is required"}), 400

        weather = get_weather(city)
        mood = detect_mood(mood_input) if mood_input else "relaxed"

        recommended_playlist = get_spotify_playlist(mood, weather)

        return jsonify({"mood": mood, "weather": weather, "playlist": recommended_playlist})

    except Exception as e:
        print("❌ Error in /get_music:", str(e))
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
