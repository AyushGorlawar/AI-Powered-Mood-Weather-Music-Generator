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
    return Non
