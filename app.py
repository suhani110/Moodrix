from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = "9888e3f9fb034daeb58f362ee5221062"
CLIENT_SECRET = "ba61d97f0130440b837f86f49fcae3bf"


def get_token():
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")


def get_song_by_emotion(emotion):
    token = get_token()

    if not token:
        return {"error": "Token error"}

    headers = {
        "Authorization": f"Bearer {token}"
    }

    query_map = {
        "happy": "happy bollywood",
        "sad": "sad hindi",
        "angry": "rock",
        "surprise": "party",
        "neutral": "lofi",
        "fear": "calm",
        "disgust": "lofi"
    }

    query = query_map.get(emotion.lower(), "chill music")

    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=10"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Spotify API failed"}

    data = response.json()
    tracks = data.get("tracks", {}).get("items", [])

    if not tracks:
        return {"error": "No songs found"}

    track = tracks[0]

    return {
        "name": track["name"],
        "artist": track["artists"][0]["name"],
        "preview_url": track.get("preview_url"),
        "spotify_url": track["external_urls"]["spotify"],
        "image": track["album"]["images"][0]["url"]
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_song/<emotion>")
def get_song(emotion):
    return jsonify(get_song_by_emotion(emotion))


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

CLIENT_ID = "9888e3f9fb034daeb58f362ee5221062"
CLIENT_SECRET = "ba61d97f0130440b837f86f49fcae3bf"


def get_token():
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")


def get_song_by_emotion(emotion):
    token = get_token()

    if not token:
        return {"error": "Token error"}

    headers = {
        "Authorization": f"Bearer {token}"
    }

    query_map = {
        "happy": "happy bollywood",
        "sad": "sad hindi",
        "angry": "rock",
        "surprise": "party",
        "neutral": "lofi",
        "fear": "calm",
        "disgust": "lofi"
    }

    query = query_map.get(emotion.lower(), "chill music")

    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=10"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Spotify API failed"}

    data = response.json()
    tracks = data.get("tracks", {}).get("items", [])

    if not tracks:
        return {"error": "No songs found"}

    track = tracks[0]

    return {
        "name": track["name"],
        "artist": track["artists"][0]["name"],
        "preview_url": track.get("preview_url"),
        "spotify_url": track["external_urls"]["spotify"],
        "image": track["album"]["images"][0]["url"]
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_song/<emotion>")
def get_song(emotion):
    return jsonify(get_song_by_emotion(emotion))


if __name__ == "__main__":
    app.run(debug=True)