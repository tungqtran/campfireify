from flask import Flask, redirect, request, session, render_template, jsonify
import requests
import os


app = Flask(__name__)
app.secret_key = "ieajsofeur8032iwjfw9da0s9du9as8409qwujadc"

CLIENT_ID = "dafa39bb45824babbe9bc69dd0b9b7d4"
CLIENT_SECRET = "c12c7c46202f4bd2962dc576ff2f3dc3"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SCOPE = "user-top-read user-read-recently-played user-library-read user-read-currently-playing"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = (
        "https://accounts.spotify.com/authorize"
        "?client_id=" + CLIENT_ID +
        "&response_type=code"
        "&redirect_uri=" + REDIRECT_URI +
        "&scope=" + SCOPE
    )

    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')

    token_url = 'https://accounts.spotify.com/api/token'

    response = requests.post("https://accounts.spotify.com/api/token", data = {
       'grant_type': 'authorization_code',
       'code': code,
       'redirect_uri': REDIRECT_URI,
       'client_id': CLIENT_ID,
       'client_secret': CLIENT_SECRET
   })

    token_info = response.json()
    access_token = token_info['access_token']
    session['token'] = access_token

    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    token = session.get('token')
    headers = {'Authorization': f'Bearer {token}'}
    user_data = requests.get('https://api.spotify.com/v1/me', headers = headers).json()

    return render_template('dashboard.html', user=user_data)

@app.route('/wrapped')
def wrapped():
    token = session.get('token')
    if not token:
        return redirect('/login')

    headers = {'Authorization': f'Bearer {token}'}

    # Get top tracks
    tracks_response = requests.get(
        'https://api.spotify.com/v1/me/top/tracks?limit=10',
        headers=headers
    )
    top_tracks = tracks_response.json().get('items', [])

    # Get top artists
    artists_response = requests.get(
        'https://api.spotify.com/v1/me/top/artists?limit=10',
        headers=headers
    )
    top_artists = artists_response.json().get('items', [])

    return render_template(
        'wrapped.html',
        tracks=top_tracks,
        artists=top_artists
    )



# campfire method and campfire html represent the currently played track for the user logged in 
@app.route('/campfire')
def campfire():
    token = session.get('token')
    
    if not token:
        return redirect('/login')


    headers = {'Authorization': f'Bearer {token}'}

    spotify_api_response = requests.get(
        'https://api.spotify.com/v1/me/player/currently-playing',
        headers = headers
    )

    if spotify_api_response.status_code == 200:
        data = spotify_api_response.json()
        if data.get('item'): #if track playing
            track = {
                'name': data['item']['name'],
                'artist': ', '.join([artist['name'] for artist in data['item']['artists']]),
                'album': data['item']['album']['name'],
                'image': data['item']['album']['images'][0]['url']
            }
            
        else: # no track playing
            track = {
                'name': "no track",
                'artist': "n/a",
                'album': "n/a",
                'image': "https://i.redd.it/kra8id3at5ld1.png"
            }
            
    else: # a status =/= 200 means something wrong happened (bad token, etc.)
        track = {
            'name': "status != 200",
            'artist': "n/a",
            'album': "n/a",
            'image': "https://i.redd.it/kra8id3at5ld1.png"
        }
        
    return render_template('campfire.html', track=track)



if __name__ == '__main__':
    app.run(debug=True)

