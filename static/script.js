function startApp() {
    document.getElementById("welcome").style.display = "none";
    document.getElementById("app").style.display = "block";
    startCamera();
}


async function startCamera() {
    const video = document.getElementById("video");

    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;

        // 🔥 simulate RANDOM emotion (for now)
        setTimeout(() => {
            const emotions = ["happy", "sad", "angry", "surprise", "neutral"];
            const randomEmotion = emotions[Math.floor(Math.random() * emotions.length)];
            handleEmotion(randomEmotion);
        }, 3000);

    } catch (err) {
        console.error(err);
        alert("Camera not working 😭");
    }
}


function handleEmotion(emotion) {
    document.getElementById("emotionText").innerText = "Emotion: " + emotion;
    changeBackground(emotion);

    fetch(`/get_song/${emotion}`)
        .then(res => res.json())
        .then(data => {

            if (data.error) {
                document.getElementById("songText").innerText = data.error;
                return;
            }

            document.getElementById("songText").innerText =
                data.name + " - " + data.artist;
            document.getElementById("albumArt").src = data.image;

            const audio = document.getElementById("audio-player");

            if (data.preview_url) {
                audio.src = data.preview_url;
                audio.play();
            } else {
                audio.src = "";
            }

            window.spotifyLink = data.spotify_url;
            document.getElementById("playBtn").style.display = "inline-block";
        });
}


function playSong() {
    if (window.spotifyLink) {
        window.open(window.spotifyLink, "_blank");
    }
}
function changeBackground(emotion) {

    const body = document.body;

    if (emotion === "happy") {
        body.style.background = "linear-gradient(135deg, #fbc2eb, #a6c1ee)";
    } 
    else if (emotion === "sad") {
        body.style.background = "linear-gradient(135deg, #2c3e50, #4ca1af)";
    } 
    else if (emotion === "angry") {
        body.style.background = "linear-gradient(135deg, #ff416c, #ff4b2b)";
    } 
    else if (emotion === "surprise") {
        body.style.background = "linear-gradient(135deg, #f7971e, #ffd200)";
    } 
    else if (emotion === "neutral") {
        body.style.background = "linear-gradient(135deg, #bdc3c7, #2c3e50)";
    } 
    else {
        body.style.background = "linear-gradient(135deg, #1e1e2f, #2a2a40)";
    }
}