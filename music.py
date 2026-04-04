import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 🔐 Your credentials
CLIENT_ID = "9888e3f9fb034daeb58f362ee5221062"
CLIENT_SECRET = "ba61d97f0130440b837f86f49fcae3bf"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# 🎧 Emotion → Music mapping
emotion_music = {
    "happy": "party songs bollywood",
    "sad": "sad songs hindi",
    "angry": "rock intense",
    "surprise": "edm hits",
    "neutral": "lofi chill",
    "fear": "calm relaxing",
    "disgust": "uplifting songs"
}

def get_song(emotion):
    query = emotion_music.get(emotion, "trending songs")
    
    results = sp.search(q=query, limit=1)
    track = results['tracks']['items'][0]

    return {
        "name": track['name'],
        "artist": track['artists'][0]['name'],
        "url": track['external_urls']['spotify'],
        "image": track['album']['images'][0]['url']
    }

# 🧪 Test
if __name__ == "__main__":
    emotion = "happy"
    song = get_song(emotion)

    print("Song:", song["name"])
    print("Artist:", song["artist"])
    print("Link:", song["url"])