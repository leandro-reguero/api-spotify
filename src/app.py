import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import base64
from requests import post, get
import json
import datetime
import matplotlib.pyplot as plt

# load the .env file variables
load_dotenv()
cid = os.environ.get("CLIENT_ID")
cet = os.environ.get("CLIENT_SECRET")


# define the function to get the access token
def get_token():
    # building the authorization string
    auth_string = cid + ":" + cet
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # referencing the url where we want to send the request
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # storing the results obtained
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# function to construct header we need for any future requests
def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

# storing the token in a variable
token = get_token()

def search_for_artist(token, artist_name):
    # defining the url where we want to get the request from
    search_endpoint = 'https://api.spotify.com/v1/search'

    # defining the headers for the auth
    headers = get_auth_header(token)

    # constructing the query string
    query = f"?q={artist_name}&type=artist&market=ES&limit=1"
    query_url = search_endpoint + query

    # obtaining and storing the results obtained
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result) == 0:
        print("No artists with this name exist...")
        return None

    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=ES"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']
    return json_result





ask_artist = str(input('Input desired artist name: '))
token = get_token()
result = search_for_artist(token, ask_artist)
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

indexes = []
names = []
pops = []
dur = []

for idx, song in enumerate(songs):
    indexes.append(idx+1)
    names.append(song['name'])
    pops.append(song['popularity'])
    delta = str(datetime.timedelta(milliseconds=song['duration_ms']))
    dur.append(delta)

df = pd.DataFrame({'Index': indexes})
df['Name'] = names
df['Popularity'] = pops
df['Duration (h, m, s)'] = dur



print(df.sort_values(by='Duration (h, m, s)', axis=0, ascending=True, inplace=True))

plt.scatter(df['Duration (h, m, s)'], df['Popularity'])
plt.xticks(rotation=45, ha='right' )
plt.tight_layout()
plt.show()
print(f"My artist of choice, Kase.O, I would say there is a slightly relevant relationship between popularity and song duration")
print("I would conclude, that, for Kase.O, popularity and song duration are somewhat directly proportional")







