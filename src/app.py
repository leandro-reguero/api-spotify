import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import base64
from requests import post
import json

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
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# function to construct header we need for any future requests
def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

# storing the token in a variable
token = get_token()

# save the address for my artist
lean_uri = 'spotify:artist:5Mtx4kiMwPhSbwVPVVR67g'
lean_address = '5Mtx4kiMwPhSbwVPVVR67g'








