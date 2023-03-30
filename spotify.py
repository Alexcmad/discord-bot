import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

client_id = os.environ.get('SPOTIFY_CLIENT')
secret = os.environ.get('SPOTIFY_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=secret))

Plink = 'https://open.spotify.com/playlist/2rjF7l4Q5LbpMJjXMXCas3?si=7ef1092083ed4aa8'

def get_playlist_id(link):
    return link.split('/')[-1]


def get_playlist_name(link):
    playlist = get_playlist_id(link)
    return sp.playlist_items(playlist_id=playlist).get('name')


def get_playlist_description(link):
    playlist = get_playlist_id(link)
    return sp.playlist_items(playlist_id=playlist).get('description')


def get_playlist_owner(link):
    playlist = get_playlist_id(link)
    return sp.playlist_items(playlist_id=playlist).get('owner').get('display_name')


def get_playlist_items(link):
    playlist = get_playlist_id(link)
    return sp.playlist_items(playlist_id=playlist)['tracks']['items']


def get_track(item):
    return item['track']


def get_artist(track):
    return track['artists'][0]['name']


def get_track_name(track):
    return track['name']


# print(get_playlist_items(Plink)[0]['track'])