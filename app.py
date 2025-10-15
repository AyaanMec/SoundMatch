import os
import json
import requests
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask app and enable CORS for React dev server
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Spotify credentials (hardcoded)
client_id = "f0d4110119954331828a1073acd87e9a"
client_secret = "a8460ff7833d4c8bb3c4af8e350d0679"

# Get the Spotify access token
def get_token():
    auth_str = client_id + ":" + client_secret
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# Search for a song on Spotify
def search_song(token, query):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": query,
        "type": "track",
        "limit": 1
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Search failed: {response.status_code}, {response.text}")
    return response.json()

# Flask route to get track info
@app.route('/track-info', methods=['POST'])
def track_info():
    data = request.get_json()
    query = data.get('query', '')
    token = get_token()
    search_results = search_song(token, query)
    tracks = search_results['tracks']['items']

    if not tracks:
        return jsonify({'error': 'No track found'}), 404

    track = tracks[0]  # top result

    # Simulated data for now
    processed = {
        "name": track["name"],
        "artist": track["artists"][0]["name"],
        "cover": track["album"]["images"][0]["url"],
        "tempo": 120,
        "energy": 0.85,
        "danceability": 0.75,
        "lyrics": [
            "This is the first line of the song.",
            "Here comes the second line now.",
            "Let’s keep the rhythm going strong.",
            "Fourth line just before the last.",
            "Final line to end the track."
        ]
    }

    return jsonify(processed)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
