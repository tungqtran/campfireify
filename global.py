import requests
import base64

def get_spotify_token(client_id, client_secret):
    auth_string = f'{client_id}:{client_secret}'
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    headers = {
        "Authorization": f"Basic {auth_base64}"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers = headers,
        data = data
    )

    return response.json()["access_token"]

def get_country_top_tracks(token, country_code):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    #Get "Top Lists" playlists for the country
    response = requests.get(
        f"https://api.spotify.come/v1/browse/categories/toplists/playlists?country={country_code}",
        headers = headers
    )
    playlists = response.json().get('playlists', {}).get('items', [])

    if not playlists:
        return []
    
    #Grab the first playlist (usually Top 50)
    playlist_id = playlists[0]['id']

    #Fetch tracks from playlist
    track_response = requests.get(
        f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
        headers=headers
    )
    tracks = track_response.json().get('items', [])
    
    track_list = []
    for t in tracks:
        track_data = t['track']
        track_list.append({
            "name": track_data['name'],
            "artist": track_data['artists'][0]['name'],
            "preview_url": track_data['preview_url'],
            "image": track_data['album']['images'][0]['url']
        })

    return track_list
    