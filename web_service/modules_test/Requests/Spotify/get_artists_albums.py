import requests

SPOTIFY_ARTIST_ALBUMS = "https://api.spotify.com/v1/artists/6Ghvu1VvMGScGpOUJBAHNH/albums"
ACCESS_TOKEN = "BQA4mntotCYIa6pKmeClM6ZvqgriS8Sl2Iel2BC32RSnLYDfM9zqms6YmTLD0gEfops3TfYTDgViDwqMHSnKhZhg7jXw6Sayu0NCAnpOwj3e2qoGyWqTxtTRrwozWWMGMDsgvFS0Z02GsA_Es7E4D9sWP_73oKrHEoO79nzUyDcgPgCFy73pJQ0EmgHCw0VbXh1mFH4y-xPOzXfzOfKQfNwktGqOdumAlS-u3F1q_0WzxLPa7IexxDH7CTpNJ4Ee"

def get_artist_albums():
    response = requests.get(
        SPOTIFY_ARTIST_ALBUMS,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    )
    json_resp = response.text

    return json_resp

print(get_artist_albums())