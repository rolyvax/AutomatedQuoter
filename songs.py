import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

class Songs:
    def __init__(self):

        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        token_path = os.getenv("TOKEN")
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                       client_secret=client_secret,
                                                       redirect_uri="http://example.com",
                                                       scope="playlist-modify-private",
                                                       show_dialog=True,
                                                       cache_path=token_path,
                                                       username="Hakan Akay",))


        user_id = sp.current_user()["id"]

        user_playlists = sp.user_playlists(user_id)
        playlist_id = user_playlists["items"][0]["id"]

        playlist_items = sp.playlist_items(playlist_id)
        song_list = [song["track"]["id"] for song in playlist_items["items"]]

        daily_song = random.choice(song_list)

        self.song_name = sp.track(daily_song)["name"]
        self.song_link = sp.track(daily_song)["external_urls"]["spotify"]

