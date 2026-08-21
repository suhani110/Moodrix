// Start app and camera
function startApp() {
    startCamera();
}

let currentEmotion = null;

// Start webcam + REAL detection
async function startCamera() {
    const video = document.getElementById("video");

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        // 🔥 Detect every 2 seconds
        setInterval(() => {
            detectEmotion(video);
        }, 2000);

    } catch (err) {
        console.error(err);
        alert("Camera not working 😭");
    }
}

// 🔥 NEW: Send frame to backend
async function detectEmotion(video) {
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    const imageData = canvas.toDataURL("image/jpeg");

    try {
        const res = await fetch("/detect_emotion", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ image: imageData })
        });

        const data = await res.json();
        const emotion = data.emotion;

        // Only update if changed
        if (emotion && emotion !== currentEmotion) {
            currentEmotion = emotion;
            handleEmotion(emotion);
        }

    } catch (err) {
        console.error("Detection error:", err);
    }
}

// Handle emotion detection and fetch song
async function handleEmotion(emotion) {
    const emotionText = document.getElementById("emotionText");
    const songText = document.getElementById("songText");
    const albumArt = document.getElementById("albumArt");
    const playBtn = document.getElementById("playBtn");
    const audio = document.getElementById("audio-player");

    emotionText.style.opacity = 0;
    songText.style.opacity = 0;
    albumArt.style.opacity = 0;

    changeBackground(emotion);

    try {
        const res = await fetch(`/get_song/${emotion}`);
        const data = await res.json();

        if (data.error) {
            songText.innerText = data.error;
            songText.style.opacity = 1;
            return;
        }

        emotionText.innerText = "Emotion: " + emotion;
        emotionText.style.opacity = 1;

        songText.innerText = `${data.name} - ${data.artist}`;
        songText.style.opacity = 1;

        albumArt.src = data.image;
        albumArt.style.opacity = 1;

        if (data.preview_url) {
            audio.src = data.preview_url;
            audio.play();
        } else {
            audio.src = "";
        }

        window.spotifyLink = data.spotify_url;
        playBtn.style.display = "inline-block";

    } catch (err) {
        console.error(err);
        songText.innerText = "Error fetching song";
        songText.style.opacity = 1;
    }
}

// Open Spotify
function playSong() {
    if (window.spotifyLink) {
        window.open(window.spotifyLink, "_blank");
    }
}

// Background
function changeBackground(emotion) {
    const body = document.body;

    switch (emotion) {
        case "happy":
            body.style.background = "linear-gradient(135deg, #fbc2eb, #a6c1ee)";
            break;
        case "sad":
            body.style.background = "linear-gradient(135deg, #2c3e50, #4ca1af)";
            break;
        case "angry":
            body.style.background = "linear-gradient(135deg, #ff416c, #ff4b2b)";
            break;
        case "surprise":
            body.style.background = "linear-gradient(135deg, #f7971e, #ffd200)";
            break;
        case "neutral":
            body.style.background = "linear-gradient(135deg, #bdc3c7, #2c3e50)";
            break;
        default:
            body.style.background = "linear-gradient(135deg, #1e1e2f, #2a2a40)";
    }
}