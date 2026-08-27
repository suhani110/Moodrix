from flask import Flask, render_template, jsonify, request
import requests
import base64
import os
import cv2
import numpy as np
from fer import FER

app = Flask(__name__)

# --- FER detector ---
detector = FER(mtcnn=False)

# --- Spotify API credentials ---
# Credentials are loaded from environment variables
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")


def get_token():
    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": f"Basic {b64_auth_str}"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")


def get_song_by_emotion(emotion):
    token = get_token()
    if not token:
        return {"error": "Token error"}

    headers = {"Authorization": f"Bearer {token}"}

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

    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=1"
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
        "spotify_url": track["external_urls"]["spotify"],
        "image": track["album"]["images"][0]["url"]
    }


# --- HOME ---
@app.route("/")
def home():
    return render_template("index.html")


# --- EMOTION DETECTION API ---
@app.route("/detect_emotion", methods=["POST"])
def detect_emotion():
    data = request.json["image"]

    # Decode base64 image
    img_data = base64.b64decode(data.split(",")[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    result = detector.detect_emotions(frame)

    if result:
        emotions = result[0]["emotions"]
        emotion = max(emotions, key=emotions.get)
    else:
        emotion = "neutral"

    return jsonify({"emotion": emotion})


# --- SONG API ---
@app.route("/get_song/<emotion>")
def get_song(emotion):
    return jsonify(get_song_by_emotion(emotion))


# --- RUN ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)