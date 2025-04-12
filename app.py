from flask import Flask, redirect, request, session, render_template
import requests
import os

app = Flask(__name__)
app.secret_key = "ieajsofeur8032iwjfw9da0s9du9as8409qwujadc"

CLIENT_ID = "dafa39bb45824babbe9bc69dd0b9b7d4"
CLIENT_SECRET = "c12c7c46202f4bd2962dc576ff2f3dc3"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SCOPE = "user-top-read"

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

    # payload = {
    #     'grant_type': 'authorization_code',
    #     'code': code,
    #     'redirect_uri': REDIRECT_URI,  
    #     'client_id': CLIENT_ID,
    #     'client_secret': CLIENT_SECRET
    # }

    # response = requests.post(token_url, data=payload)
    # token_info = response.json()
    
    # session['token'] = token_info.get('access_token')

    # return redirect('/dashboard')



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

    return f"Hello, {user_data['display_name']}!"

if __name__ == '__main__':
    app.run(debug=True)