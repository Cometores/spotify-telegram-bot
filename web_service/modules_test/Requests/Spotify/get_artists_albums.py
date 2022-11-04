import requests

SPOTIFY_ARTIST_ALBUMS = "https://api.spotify.com/v1/artists/6Ghvu1VvMGScGpOUJBAHNH/albums"
SPOTIFY_AlBUM_TRACKS = "https://api.spotify.com/v1/albums/0FqxYHewG9WU9uaAbuzGtk/tracks"

ACCESS_TOKEN = "BQAiqiXxO6cMbHOT4MGypUhVvFh40R28E3M51G73DMp06x5yqrRj-ecE1dQMm4obtomA5qqdgUsWK4czpkeos-8_VcsbmTtIbpMhXj6eBJXjPFegKmgKb1gUWaA1MlS-QJ6zwO1rjox5Sd_1gJGTckxPjLNJVUckemPwKKXeN2q960O9MPv0u8ba4prsjjRyT6M"

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