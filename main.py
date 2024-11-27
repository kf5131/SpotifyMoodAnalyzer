import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import platform
import subprocess

# Load environment variables
load_dotenv()

# Configure Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Initialize Spotify client with necessary permissions
scope = "user-library-read playlist-read-private playlist-modify-public user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    open_browser=True,
    cache_path=".spotifycache"
))

def focus_browser():
    """Switch focus to the default web browser."""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        subprocess.call(["osascript", "-e", 'tell application "Safari" to activate'])
    elif system == "Windows":
        import win32gui
        import win32com.client
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.AppActivate("Chrome")  # Or the name of your default browser
        
    elif system == "Linux":
        # This might not work on all Linux distributions
        subprocess.call(["wmctrl", "-a", "Chrome"])  # Or the name of your default browser
    
    else:
        print("Automatic focus switching not supported on this operating system.")

def analyze_playlist_mood(playlist_id):
    """Analyze the mood of a playlist using audio features."""
    tracks = sp.playlist_tracks(playlist_id)
    track_ids = [track['track']['id'] for track in tracks['items'] if track['track'] is not None]
    audio_features = sp.audio_features(track_ids)
    
    # Filter out None values from audio features
    audio_features = [f for f in audio_features if f is not None]
    
    # Check if we have any valid tracks to analyze
    if not audio_features:
        return {
            'valence': 0,
            'energy': 0,
            'danceability': 0
        }
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(audio_features)
    
    # Calculate average mood metrics
    mood_metrics = {
        'valence': df['valence'].mean(),
        'energy': df['energy'].mean(),
        'danceability': df['danceability'].mean()
    }
    return mood_metrics

def create_mood_playlist(mood_type):
    """Create a new playlist based on mood type (happy, sad, energetic, calm)."""
    user_id = sp.current_user()['id']
    
    # Define mood parameters
    mood_params = {
        'happy': {'valence': 0.7, 'energy': 0.7},
        'sad': {'valence': 0.3, 'energy': 0.3},
        'energetic': {'valence': 0.6, 'energy': 0.8},
        'calm': {'valence': 0.5, 'energy': 0.3}
    }
    
    # Create new playlist
    playlist = sp.user_playlist_create(
        user_id, 
        f"My {mood_type.capitalize()} Playlist",
        public=True,
        description=f"Auto-generated {mood_type} mood playlist"
    )
    
    return playlist['id'], playlist['name']

def visualize_listening_history():
    """Generate visualization of user's music taste over time."""
    # Get user's top tracks
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='medium_term')
    track_ids = [track['id'] for track in top_tracks['items']]
    audio_features = sp.audio_features(track_ids)
    
    # Create visualization
    df = pd.DataFrame(audio_features)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='valence', y='energy')
    plt.title("Music Mood Distribution")
    plt.xlabel("Valence (Happiness)")
    plt.ylabel("Energy")
    plt.savefig('mood_distribution.png')
    plt.close()

def main():
    try:
        # Trigger authentication and switch focus to browser
        sp.current_user()
        focus_browser()
        
        # First verify we can connect to Spotify
        user = sp.current_user()
        print(f"Connected to Spotify as {user['display_name']}")
        
        # Get user's playlists instead of using a hardcoded ID
        playlists = sp.current_user_playlists(limit=1)
        if len(playlists['items']) > 0:
            playlist_id = playlists['items'][0]['id']
            print(f"Analyzing playlist: {playlists['items'][0]['name']}")
            
            # Analyze the first playlist found
            mood_metrics = analyze_playlist_mood(playlist_id)
            print("Playlist Mood Metrics:", mood_metrics)
        else:
            print("No playlists found in your account")
        
        # Create a new mood-based playlist
        new_playlist_id, new_playlist_name = create_mood_playlist('happy')
        print(f"Created new playlist: {new_playlist_name} (ID: {new_playlist_id})")
        
        # Generate visualization
        visualize_listening_history()
        print("Visualization saved as 'mood_distribution.png'")
        
    except spotipy.SpotifyException as e:
        print(f"Spotify API error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
