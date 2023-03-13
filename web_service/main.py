from flask import Flask

from web_service.spotify_api.spotify_api import SpotifyClient

app = Flask(__name__)

@app.route("/index")
@app.route("/")
def index():
    return "Spotify API"

@app.route("/albums_by/<artist_name>")
def get_albums_by_artist(artist_name: str):
    albums = spotify_client.get_albums_by_artist(artist_name)
    return albums

''' Запуск приложения '''
if __name__ == "__main__":
    spotify_client = SpotifyClient()
    app.run(debug=True)