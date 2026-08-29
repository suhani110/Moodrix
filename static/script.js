// Start app and camera
function startApp() {
    startCamera();
}

let currentEmotion = null;

// Start webcam + REAL emotion detection
async function startCamera() {
    const video = document.getElementById("video");

    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: true
        });

        video.srcObject = stream;

        // Make sure the video has actually started
        await video.play();

        // Continuously detect emotion, but NEVER overlap requests
        while (true) {
            await detectEmotion(video);

            // Wait 3 seconds before the next detection
            await new Promise(resolve => setTimeout(resolve, 3000));
        }

    } catch (err) {
        console.error("Camera error:", err);
        alert("Camera not working 😭");
    }
}


// Send one frame to backend for emotion detection
async function detectEmotion(video) {

    // Don't send an empty frame
    if (!video.videoWidth || !video.videoHeight) {
        console.log("Video not ready yet...");
        return;
    }

    const canvas = document.createElement("canvas");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");

    // Capture current webcam frame
    ctx.drawImage(
        video,
        0,
        0,
        canvas.width,
        canvas.height
    );

    // Convert image to base64
    const imageData = canvas.toDataURL("image/jpeg", 0.8);

    try {

        console.log("Sending frame for emotion detection...");

        const res = await fetch("/detect_emotion", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                image: imageData
            })
        });

        if (!res.ok) {
            throw new Error(
                `Server returned ${res.status}`
            );
        }

        const data = await res.json();

        console.log("Emotion response:", data);

        const emotion = data.emotion;

        if (emotion && emotion !== currentEmotion) {
            currentEmotion = emotion;

            console.log("New emotion detected:", emotion);

            handleEmotion(emotion);
        }

    } catch (err) {
        console.error("Detection error:", err);
    }
}


// Handle detected emotion and fetch song
async function handleEmotion(emotion) {

    const emotionText =
        document.getElementById("emotionText");

    const songText =
        document.getElementById("songText");

    const albumArt =
        document.getElementById("albumArt");

    const playBtn =
        document.getElementById("playBtn");

    const audio =
        document.getElementById("audio-player");


    // Hide previous result
    emotionText.style.opacity = 0;
    songText.style.opacity = 0;
    albumArt.style.opacity = 0;


    // Change background
    changeBackground(emotion);


    try {

        console.log("Getting song for:", emotion);

        const res = await fetch(
            `/get_song/${emotion}`
        );

        if (!res.ok) {
            throw new Error(
                `Song API returned ${res.status}`
            );
        }

        const data = await res.json();

        console.log("Song response:", data);


        // Spotify/API error
        if (data.error) {

            songText.innerText = data.error;
            songText.style.opacity = 1;

            return;
        }


        // Show emotion
        emotionText.innerText =
            "Emotion: " + emotion;

        emotionText.style.opacity = 1;


        // Show song
        songText.innerText =
            `${data.name} - ${data.artist}`;

        songText.style.opacity = 1;


        // Show album artwork
        if (data.image) {

            albumArt.src = data.image;
            albumArt.style.opacity = 1;
        }


        // Spotify preview
        if (data.preview_url) {

            audio.src = data.preview_url;

            try {
                await audio.play();
            } catch (err) {
                console.log(
                    "Browser blocked automatic audio playback."
                );
            }

        } else {

            audio.src = "";
        }


        // Spotify button
        window.spotifyLink =
            data.spotify_url;

        playBtn.style.display =
            "inline-block";


    } catch (err) {

        console.error(
            "Song fetching error:",
            err
        );

        songText.innerText =
            "Error fetching song";

        songText.style.opacity = 1;
    }
}


// Open song on Spotify
function playSong() {

    if (window.spotifyLink) {

        window.open(
            window.spotifyLink,
            "_blank"
        );
    }
}


// Change background according to emotion
function changeBackground(emotion) {

    const body = document.body;

    switch (emotion) {

        case "happy":

            body.style.background =
                "linear-gradient(135deg, #fbc2eb, #a6c1ee)";

            break;


        case "sad":

            body.style.background =
                "linear-gradient(135deg, #2c3e50, #4ca1af)";

            break;


        case "angry":

            body.style.background =
                "linear-gradient(135deg, #ff416c, #ff4b2b)";

            break;


        case "surprise":

            body.style.background =
                "linear-gradient(135deg, #f7971e, #ffd200)";

            break;


        case "neutral":

            body.style.background =
                "linear-gradient(135deg, #bdc3c7, #2c3e50)";

            break;


        case "fear":

            body.style.background =
                "linear-gradient(135deg, #232526, #414345)";

            break;


        case "disgust":

            body.style.background =
                "linear-gradient(135deg, #134e5e, #71b280)";

            break;


        default:

            body.style.background =
                "linear-gradient(135deg, #1e1e2f, #2a2a40)";
    }
}