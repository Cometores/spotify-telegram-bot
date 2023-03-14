from flask import Flask

from web_service.spotify_api.spotify_api import SpotifyClient

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


if __name__ == "__main__":
    spotify_client = SpotifyClient()
    app.run(debug=True)
