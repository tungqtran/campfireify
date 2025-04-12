from dotenv import load_dotenv
import os
import base64
from requests import post, get  
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

print(client_id,client_secret)

#authorization tokens for spotify
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }

    data = {"grant_type": "client_credentials"}
    results = post(url, headers=headers, data=data)
    json_result = json.loads(results.content)
    token = json_result["access_token"]
    return token

#  Authorization header for requests
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

 
#search for artists, can be changed to different measures
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist exists")
        return None
    return json_result[0]
  
    print(json_result)

#search for artists, can be changed to different measures
def search_for_tracks(token, tracks_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={tracks_name}&type=track&limit=5"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("No artist exists")
        return None
    return json_result[0]

#getter for tracks
def get_songs_by_tracks(token, tracks_name):
    url = f"https://api.spotify.com/v1/artists/{tracks_name}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result


#looking for a specific artist, passing in artist_id, then findng its top tracks, any 2 digit country code
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


    
token = get_token()
result = search_for_artist(token, "ACDC") #change to different artists to test or view songs
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

#printing top 10 songs, in country by specific artist (changes by year or country)
for idx,song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}") 


#tracks = search_for_tracks(token, "Blinding Lights")

#for t in tracks:
   # print(f"{t['name']} by {t['artists'][0]['name']} — URI: {t['uri']}")


#print(result["name"])
#print(songs)
#print(token)

