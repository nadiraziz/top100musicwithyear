from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(

        client_id="83c2155a23044e39a585f9da1324aa9c",
        client_secret=" 9ab8205cd4ed42cda6e1983c5bc396f2",)
    )


date = input("Enter The year in YYYY-MM-DD = ")


response = requests.get(URL + date)
website_html = response.text

soup = BeautifulSoup(website_html, 'html.parser')
music_list = soup.find_all("span", class_="chart-element__information__song")
top_music = [music.getText() for music in music_list]
print(top_music)

with open('top_music.txt', 'w') as file:
    count = 1
    for music in top_music:
        file.write(f"{count}) {music}\n")
        count += 1

#Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="83c2155a23044e39a585f9da1324aa9c",
        client_secret=" 9ab8205cd4ed42cda6e1983c5bc396f2",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

#Searching Spotify for songs by title
song_uris = []
year = date.split("-")[0]
for song in top_music:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")



print(song_uris)

#Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

