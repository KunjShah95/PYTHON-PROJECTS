import requests
import json
import spacy
from googletrans import Translator
import aiml
import speech_recognition as sr
import pyttsx3
import os

# Constants
SPOTIFY_API_URL = "https://api.spotify.com/v1"
ACCESS_TOKEN = "[REDACTED:Generic API Key]"  # You will need to implement OAuth to get this token
LASTFM_API_URL = "http://ws.audioscrobbler.com/2.0/"
TRANSLATOR = Translator()
nlp = spacy.load("en_core_web_sm")

# Initialize AIML kernel
kernel = aiml.Kernel()
kernel.learn("music_assistant.aiml")  # Load your AIML file

# Initialize text-to-speech
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

def handle_api_error(response):
    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        return "There was an error with the music service."

# User Authentication
def authenticate_user(username, password):
    # Placeholder for user authentication logic
    # In a real application, this would check against a database
    if username == "user" and password == "pass":
        return True
    return False

# User Preferences Management
def save_user_preferences(user_id, preferences):
    with open(f"{user_id}_preferences.json", "w") as f:
        json.dump(preferences, f)

def load_user_preferences(user_id):
    try:
        with open(f"{user_id}_preferences.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Playlist Management
def create_playlist(user_id, playlist_name):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "name": playlist_name,
        "public": False
    }
    response = requests.post(f"{SPOTIFY_API_URL}/users/{user_id}/playlists", headers=headers, json=data)
    if response.status_code == 201:
        speak(f"Playlist '{playlist_name}' created successfully.")
        return f"Playlist '{playlist_name}' created successfully."
    else:
        return handle_api_error(response)

def get_playlists(user_id):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    response = requests.get(f"{SPOTIFY_API_URL}/users/{user_id}/playlists", headers=headers)
    if response.status_code == 200:
        playlists = response.json()['items']
        return [playlist['name'] for playlist in playlists]
    else:
        return handle_api_error(response)

# Music Recommendations
def get_recommendations(seed_tracks):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "seed_tracks": seed_tracks,
        "limit": 10
    }
    response = requests.get(f"{SPOTIFY_API_URL}/recommendations", headers=headers, params=params)
    if response.status_code == 200:
        recommendations = response.json()['tracks']
        return [track['name'] + " by " + track['artists'][0]['name'] for track in recommendations]
    else:
        return handle_api_error(response)

# Enhanced Search Functionality
def search_song(query):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    params = {
        "q": query,
        "type": "track,album,artist",
        "limit": 5
    }
    response = requests.get(f"{SPOTIFY_API_URL}/search", headers=headers, params=params)
    if response.status_code == 200:
        results = response.json()
        tracks = results.get('tracks', {}).get('items', [])
        return [(track['name'], track['artists'][0]['name']) for track in tracks]
    else:
        return handle_api_error(response)

# Favorites Management
def add_to_favorites(user_id, song_name):
    favorites = load_user_preferences(user_id).get('favorites', [])
    favorites.append(song_name)
    preferences = {'favorites': favorites}
    save_user_preferences(user_id, preferences)
    return f"{song_name} has been added to your favorites."

def get_favorites(user_id):
    return load_user_preferences(user_id).get('favorites', [])

# Song Playback Control (Placeholder)
def play_song(song_name):
    # This function would require additional setup for playback control
    return f"Playing {song_name} now."

def pause_song():
    # Placeholder for pausing the song
    return "Song paused."

def skip_song():
    # Placeholder for skipping the song
    return "Skipped to the next song."

# Main Loop
def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    if not authenticate_user(username, password):
        print("Authentication failed.")
        return

    user_id = username  # Use username as user_id for simplicity

    while True:
        command = listen()
        if command:
            response = kernel.respond(command)
            speak(response)
            
            # Example command handling
            if "create playlist" in command.lower():
                playlist_name = command.split("create playlist")[-1].strip()
                response = create_playlist(user_id, playlist_name)
                speak(response)
            elif "recommend songs" in command.lower():
                seed_tracks = "track_id"  # Replace with actual track ID
                recommendations = get_recommendations(seed_tracks)
                speak("Here are some recommendations: " + ", ".join(recommendations))
            elif "search for" in command.lower():
                query = command.split("search for")[-1].strip()
                results = search_song(query)
                if results:
                    speak("I found the following: " + ", ".join([f"{name} by {artist}" for name, artist in results]))
                else:
                    speak("No results found.")
            elif "add to favorites" in command.lower():
                song_name = command.split("add to favorites")[-1].strip()
                response = add_to_favorites(user_id, song_name)
                speak(response)
            elif "show favorites" in command.lower():
                favorites = get_favorites(user_id)
                if favorites:
                    speak("Your favorite songs are: " + ", ".join(favorites))
                else:
                    speak("You have no favorite songs.")
            elif "play" in command.lower():
                song_name = command.split("play")[-1].strip()
                response = play_song(song_name)
                speak(response)
            elif "pause" in command.lower():
                response = pause_song()
                speak(response)
            elif "skip" in command.lower():
                response = skip_song()
                speak(response)

if __name__ == "__main__":
    main()
