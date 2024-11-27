# Spotify Music Mood Analyzer

This application analyzes your Spotify listening habits and creates personalized mood-based playlists. The app authenticates users through Spotify's OAuth2 flow and examines their playlists and listening history. Using Spotify's audio features API, it generates custom playlists based on mood characteristics. The application includes a callback URL system to handle the OAuth token exchange process. Additionally, it provides visual analytics to track how your music taste evolves over time.

## Requirements

- Python 3.10 or later
- Spotify account
- Spotify API credentials (client ID and client secret)
- Spotify Redirect URI (e.g., http://localhost:8888/callback)
- Python packages listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kf5131/spotify-music-mood-analyzer.git
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file and add your Spotify API credentials:
     ```bash
     SPOTIPY_CLIENT_ID=your_client_id
     SPOTIPY_CLIENT_SECRET=your_client_secret
     SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
     ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Follow the instructions in the terminal to authenticate with Spotify and authorize the application.

3. The application will analyze your listening habits and create a new mood-based playlist.

4. You can view the new playlist in your Spotify account and in the terminal. Additionally, you can view mood_distribution.png in the same folder as the script was run.
