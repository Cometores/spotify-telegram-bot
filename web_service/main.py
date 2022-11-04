from flask import Flask

from web_service.modules_test.Requests.Spotify.get_artists_albums import get_artist_albums

app = Flask(__name__)

@app.route("/index")
@app.route("/")
def index():
    get_artist_albums()
    return "Тест Requests"


''' Запуск приложения '''
if __name__ == "__main__":
    app.run(debug=True)