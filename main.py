from bs4 import BeautifulSoup
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "MY_CLIENT_ID"
CLIENT_SECRET = "MY_CLIENT_SECRET"
URL = "https://www.billboard.com/charts/hot-100/"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_DISPLAY_NAME = "MY_DISPLAY_NAME"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username=SPOTIFY_DISPLAY_NAME,
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

# Spotify own auth, not needed for this project since we are using spotipy
# header = {
#     'Content-Type': 'application/x-www-form-urlencoded'
# }
#
# body = {
#     'grant_type': 'client_credentials',
#     'client_id': CLIENT_ID,
#     'client_secret': CLIENT_SECRET,
# }

# spotify_response = requests.post(url=SPOTIFY_TOKEN_URL, headers=header, data=body)
# print(f"Your token is {spotify_response.json()['access_token']}")
# print(f"Your token expires in {spotify_response.json()['expires_in']} seconds")

date_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
print(f"Your date is {date_input}. Fetching data...")

response = requests.get(f"{URL}/{date_input}/")
# response = requests.get("https://www.billboard.com/charts/hot-100/2000-08-12/")
billboard_html = response.text

soup = BeautifulSoup(billboard_html, "html.parser")
song_titles = soup.select("li ul li h3")
# print(song_titles)

# playlist = [song.getText().strip() for song in song_title]

song_name = []
for song in song_titles:
    result = song.getText().strip()
    # print(song_name)
    song_name.append(result)
print(song_name)

song_uris = []
year = date_input.split("-")[0]
for song in song_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date_input} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)