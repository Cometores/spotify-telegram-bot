import json
from os import environ
from flask import Flask
from spotify_service.spotify_api.spotify_api import SpotifyClient

app = Flask(__name__)


@app.route("/index")
@app.route("/")
def index():
    return "Spotify API"


@app.route("/albums_by_artist/<artist_name>")
def get_albums_by_artist(artist_name: str):
    albums = spotify_client.get_albums_by_artist(artist_name)
    return albums


@app.route("/tracks_from_album/<album_name>")
def get_tracks_from_album(album_name: str):
    tracks = spotify_client.get_tracks_from_album(album_name)
    return tracks


@app.route("/top_tracks_by_artist/<artist_name>")
def get_top_tracks_by_artist(artist_name: str):
    top_tracks = spotify_client.get_top_tracks_by_artist(artist_name)
    return top_tracks


# if __name__ == "__main__":
#     settings_file_path = environ.get('settings_file_path') \
#         if environ.get('settings_file_path') is not None else "settings.json"
#
#     with open(settings_file_path) as settings_file:
#         settings = json.load(settings_file)
#
#     spotify_client = SpotifyClient(settings)
#     app.run(debug=True)


settings_file_path = environ.get('settings_file_path') \
    if environ.get('settings_file_path') is not None else "settings.json"
with open(settings_file_path) as settings_file:
    settings = json.load(settings_file)
spotify_client = SpotifyClient(settings)
#app.run(debug=True)