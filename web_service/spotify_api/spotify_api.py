import datetime
import json
import requests
import base64


class AccessToken:
    value: str = None
    valid_to: datetime.datetime = None

    def __init__(self, value: str, valid_to: datetime.datetime):
        self.value = value
        self.valid_to = valid_to

    def __str__(self):
        return f"AccessToken value: {self.value}\n" \
               f"valid to: {self.valid_to.time()}"


class SpotifyClient:
    access_token: AccessToken = None
    CLIENT_ID: str = None
    CLIENT_SECRET: str = None

    def __init__(self):
        # Extracting a secret from a file
        with open("settings.json") as settings_file:
            settings = json.load(settings_file)
            self.CLIENT_ID = settings["CLIENT_ID"]
            self.CLIENT_SECRET = settings["CLIENT_SECRET"]

        self.set_acces_token()


    '''Obtaining an access-token for the Spotify API'''
    def set_acces_token(self):
        # Auth-Login information is transmitted in base64 format
        auth_header_bytes = base64.b64encode(bytes(
            (self.CLIENT_ID + ":" + self.CLIENT_SECRET), 'utf-8'))
        auth_header = auth_header_bytes.decode('utf-8')

        url = "https://accounts.spotify.com/api/token?json=true"
        payload = {'grant_type': 'client_credentials'}
        headers = {
            f'Authorization': f'Basic {auth_header}'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        value = response.json()["access_token"]
        _expires_in = response.json()["expires_in"]
        valid_to = datetime.datetime.now() + datetime.timedelta(seconds=_expires_in)

        self.access_token = AccessToken(value, valid_to)


    '''Preparing a request auth-header token'''
    def prepare_auth_header(self):
        if self.access_token is None or datetime.datetime.now() > self.access_token.valid_to:
            self.set_access_token()
        auth_header = "Bearer " + self.access_token.value
        return auth_header


    '''Looking for id by name *'''
    def get_id(self, search_type: str, name: str) -> str:
        # ПОКА ЧТО РАБОТАЕТ ТОЛЬКО ПОИСК ПО АРТИСТ
        url = "https://api.spotify.com/v1/search"

        params = {
            "type": search_type,
            "q": name
        }
        auth_header = self.prepare_auth_header()
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, params=params)
        return (response.json()["artists"]["items"][0]["id"])


    '''Get all tracks of a particular album'''
    def get_tracks_by_album(self, album_name: str) -> list[str]:
        # НЕ РАБОТАЕТ, ИЗ-ЗА get_id
        id = self.get_id("??????", album_name)
        url = f"https://api.spotify.com/v1/albums/{id}/tracks"

        auth_header = self.prepare_auth_header()
        response = requests.get(
            url,
            headers={
                "Authorization": auth_header
            }
        )
        json_resp = response.text

        return json_resp


    '''Get all albums by a certain artist'''
    def get_albums_by_artist(self, artist_name: str) -> list[str]:
        id = self.get_id("artist", artist_name)
        url = f"https://api.spotify.com/v1/artists/{id}/albums"

        auth_header = self.prepare_auth_header()
        response = requests.get(
            url,
            headers={
                "Authorization": auth_header
            }
        )

        json_resp = response.json()["items"]
        albums = [item["name"] for item in json_resp] # MAX Len 20 - исправить

        return albums


def test():
    spotify_client = SpotifyClient()
    print(spotify_client.get_albums_by_artist("Skeler"))


test()
