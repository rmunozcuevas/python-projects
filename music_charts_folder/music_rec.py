from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from flask import Flask, jsonify, request, render_template, send_from_directory
import time

# --- Load environment variables ---
# --- flask --app music_rec.py run ---
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

if not client_id or not client_secret:
    raise ValueError("CLIENT_ID or CLIENT_SECRET not found in .env")

# --- Token management ---
spotify_token = None
token_expires_at = 0

def get_token():
    global spotify_token, token_expires_at
    if spotify_token is None or time.time() >= token_expires_at:
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        json_result = json.loads(result.content)

        spotify_token = json_result["access_token"]
        token_expires_at = time.time() + json_result["expires_in"] - 60

    return spotify_token

def get_auth_header():
    return {"Authorization": "Bearer " + get_token()}

# --- Spotify API helpers ---
def search_for_artist(artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header()
    query = f"q={artist_name}&type=artist&limit=1"
    result = get(url + "?" + query, headers=headers)
    items = json.loads(result.content)["artists"]["items"]
    return items[0] if items else None

def get_songs_by_artist(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header()
    result = get(url, headers=headers)
    return json.loads(result.content)["tracks"]

def top_ten(artist_name):
    artist = search_for_artist(artist_name)
    if not artist:
        return None

    artist_id = artist["id"]
    artist_photo = artist["images"][0]["url"] if artist["images"] else None
    songs = get_songs_by_artist(artist_id)

    top_tracks = [
        {
            "name": song["name"],
            "album": song["album"]["name"],
            "preview_url": song["preview_url"],
            "spotify_url": song["external_urls"]["spotify"]
        }
        for song in songs[:10]
    ]

    return {
        "artist_name": artist["name"],
        "artist_photo": artist_photo,
        "top_tracks": top_tracks
    }

def more_popular(artist1_name, artist2_name):
    artist_one = search_for_artist(artist1_name)
    artist_two = search_for_artist(artist2_name)

    if not artist_one or not artist_two:
        return None

    return artist_one if artist_one["popularity"] > artist_two["popularity"] else artist_two

# def mash_playlist(p_one, p_two):
#   play_one = 


# --- Flask setup ---
app = Flask(__name__)

@app.route('/styles/<path:filename>')
def static_styles(filename):
    return send_from_directory('styles', filename)

@app.route('/scripts/<path:filename>')
def static_scripts(filename):
    return send_from_directory('scripts', filename)


@app.route("/")
def home():
    # Just render homepage with input form
    return render_template("music.html")

@app.route("/top-ten")
def top_ten_route():
    artist_name = request.args.get("artist")
    if not artist_name:
        return "Please enter an artist name", 400

    result = top_ten(artist_name)
    if result is None:
        return jsonify({"error": "Artist not found"}), 404

    return render_template("music.html", data=result)

@app.route("/compare")
def compare_route():
    artist1 = request.args.get("a1")
    artist2 = request.args.get("a2")

    if not artist1 or not artist2:
        return jsonify({"error": "Please provide ?a1=artist1&a2=artist2"}), 400

    winner = more_popular(artist1, artist2)
    if not winner:
        return jsonify({"error": "One or both artists not found"}), 404

    return jsonify({
        "more_popular": winner["name"],
        "popularity": winner["popularity"]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)
