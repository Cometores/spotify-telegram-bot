import datetime
import requests
import base64
from dataclasses import dataclass
from typing import List, Dict


@dataclass
class AccessToken:
    value: str = None
    valid_to: datetime.datetime = None

    def __str__(self):
        return f"AccessToken value: {self.value}\n" \
               f"valid to: {self.valid_to.time()}"


class SpotifyClient:
    access_token: AccessToken = None
    CLIENT_ID: str = None
    CLIENT_SECRET: str = None

    def __init__(self, settings: Dict[str, str]):
        self.CLIENT_ID = settings["CLIENT_ID"]
        self.CLIENT_SECRET = settings["CLIENT_SECRET"]
        self.set_access_token()

    def set_access_token(self):
        # Auth-Login information is transmitted in base64 format
        auth_header_bytes = base64.b64encode(bytes(
            (self.CLIENT_ID + ":" + self.CLIENT_SECRET), 'utf-8'))
        auth_header = auth_header_bytes.decode('utf-8')

        url = "https://accounts.spotify.com/api/token?json=true"
        payload = {'grant_type': 'client_credentials'}
        headers = {
            f'Authorization': f'Basic {auth_header}'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        value = response["access_token"]
        _expires_in = response["expires_in"]
        valid_to = datetime.datetime.now() + datetime.timedelta(seconds=_expires_in)

        self.access_token = AccessToken(value, valid_to)

    def prepare_auth_header(self) -> str:
        if self.access_token is None or datetime.datetime.now() > self.access_token.valid_to:
            self.set_access_token()
        auth_header = "Bearer " + self.access_token.value
        return auth_header

    def get_id(self, search_type: str, name: str) -> str:
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
        return response.json()[search_type + "s"]["items"][0]["id"]

    def get_tracks_from_album(self, album_name: str) -> List[str]:
        id = self.get_id("album", album_name)
        url = f"https://api.spotify.com/v1/albums/{id}/tracks"

        auth_header = self.prepare_auth_header()
        response = requests.get(
            url,
            headers={
                "Authorization": auth_header
            }
        )
        json_resp = response.json()["items"]
        tracks = [item["name"] for item in json_resp]

        return tracks

    def get_albums_by_artist(self, artist_name: str) -> List[str]:
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
        albums = [item["name"] for item in json_resp]  # MAX Len 20 - исправить

        return albums

    def get_top_tracks_by_artist(self, artist_name: str, market="ES") -> List[str]:
        id = self.get_id("artist", artist_name)
        url = f"https://api.spotify.com/v1/artists/{id}/top-tracks?market={market}"

        auth_header = self.prepare_auth_header()
        response = requests.get(
            url,
            headers={
                "Authorization": auth_header
            }
        )

        json_resp = response.json()["tracks"]
        top_tracks = [item["name"] for item in json_resp]  # MAX Len 20 - исправить

        return top_tracks
