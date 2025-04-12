from dotenv import load_dotenv
import os
import base64
from requests import post, get  
import json

 

#gets the .env file, to use client_id and client_secret
load_dotenv()

#gets the environment variables and assigns it to local variable
client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET")


#prepares authorization for access tokens for spotify
def get_token(): 
    auth_string = client_id + ":" + client_secret #creates a combined string for id and secret
    auth_bytes = auth_string.encode('utf-8') #converts this code into bytes
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8") #base64 encoded, because Spotify requires this format, then converted back to a UTF-8 String

    #this url is a specific url from spotify where you can send your credentials and get a specific access token
    url = "https://accounts.spotify.com/api/token" #endPoint (specific URL where you send requests to get data) for spotify token

    #send http headers (like labels on a package, tells recipient how to handle the package)
    headers = {
        "Authorization": "Basic " + auth_base64, #tells spotify who are you; basic means using just username/password (client id and client secert)
        "Content-Type": "application/x-www-form-urlencoded" #how you data is formatted in request

    }

    #requesting the token, actually making it work!!
    data = {"grant_type": "client_credentials"} #what kind of token you are asking for, using "Client Credentials Flow." *which is for apps that don't act on behalf of a user (just the app itself)*??
    
    #This is like sending a sealed envelope to Spotify saying:
    #"Hi Spotify, here’s my ID (in the headers), and I’d like a token please (grant_type in the body)."
    results = post(url, headers=headers, data=data) #sends spotify post request to endpoint

    #results.content gives you the raw data in JSON(java script)
    #json.load converts into Python
    json_result = json.loads(results.content) 

    #grabs the actual token
    token = json_result["access_token"]
    return token

#  Authorization header for requests (SUPER IMPORTANT for anything API!!)
def get_auth_header(token):
    #Authorization: tells who you are
    #Bearer: type of token you are using
    return {"Authorization": "Bearer " + token} #pass into everyheader to prove you can make the request

 
#search for artists, can be changed to different measures
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search" #endpoint for searching artists, albums, tracks, etc

    headers = get_auth_header(token) #makes the authorization header

    #q={artist_name}: the search term
    #type=artist: you specifically searching for artists
    #limit=1: only return 1 result
    query = f"?q={artist_name}&type=artist&limit=1" 

    query_url = url + query #formats a full URL request
    result = get(query_url, headers=headers) #sends a GET request with full URL and headers
    json_result = json.loads(result.content)["artists"]["items"] #converts JSON code into Python; gives you matching artists (items: name, id, genre, etc)
    
    #edge case: no artists found
    if len(json_result) == 0: 
        print("No artist exists")
        return None
    return json_result[0] #only returns the first since the limit is 1
  
    print(json_result)



#looking for a specific artist, passing in artist_id, then findng its top tracks, any 2 digit country code
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US" #builds URL, spotify endpoint with specified country
   
   #same code as before, creating header, parsing JSON
    headers = get_auth_header(token) 
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"] #pulls specifically the tracks of "top tracks of the country"
    return json_result



#CHANGE THIS TO TEST DIFFERENT TRACKS

#search for artists, can be changed to different measures
def search_for_tracks(token, tracks_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={tracks_name}&type=track&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if len(json_result) == 0:
        print("No artist exists")
        return None
    return json_result[0]

#getter for tracks
def get_songs_by_tracks(token, tracks_name):
    url = f"https://api.spotify.com/v1/tracks/{tracks_name}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result







#MAIN? running and applying the methods
    
token = get_token() #retrieves the access token

#result holds a "dictionary" of the artist's info
artist_result = search_for_artist(token, "ACDC") #token is passed to authorize, and you can search for specific artist
artist_id = artist_result["id"] #fetches the specific artist ID from results dictionary
songs = get_songs_by_artist(token, artist_id) 

#f string is a formatted string
#printing by song popularity, and top 10 songs

for song in songs:
 print(f"{song['name']} (Popularity: {song['popularity']})")




#for specific tracks
track_results = search_for_tracks(token, "Blank Space")
track_name = track_results["name"]
track_artistName = track_results["artists"][0]["name"]
track_albumName = track_results["album"]["name"]
track_duration = track_results["duration_ms"]/60000

track_results_string = f"Song Name: {track_name}\nArtist Name: {track_artistName}\nAlbum Name: {track_albumName}\nDuration of Song: {track_duration}"
print(track_results_string)








 


#print(result["name"])
#print(songs)
#print(token)

