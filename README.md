# 🎵 Moodrix — Real-Time Emotion-Based Music Recommendation System

Moodrix is a **real-time emotion-based music recommendation web application** that detects a user's facial emotion through their camera and recommends music based on their current mood.

The project combines **Computer Vision, Machine Learning, and the Spotify API** to create a personalized music experience.

---

## ✨ Features

* 🎭 Real-time facial emotion detection
* 📷 Camera-based emotion recognition
* 🧠 CNN-based emotion classification
* 👤 Facial analysis using DeepFace
* 🎵 Emotion-to-music genre mapping
* 🎧 Music recommendations using the Spotify API
* 🌐 Web-based interface
* 🚀 Flask backend
* ☁️ Deployment-ready configuration

---

## 🧠 How Moodrix Works

Moodrix follows a simple pipeline:

```text
User
  ↓
Web Camera
  ↓
Image Capture
  ↓
OpenCV
  ↓
Facial Emotion Detection
  ↓
CNN / DeepFace
  ↓
Detected Emotion
  ↓
Emotion → Music Genre Mapping
  ↓
Spotify API
  ↓
Music Recommendations
```

The system analyzes the user's facial expression, identifies the most likely emotion, and maps that emotion to a suitable music genre.

For example:

```text
Happy      → Pop / Dance
Sad        → Acoustic / Calm
Angry      → Rock
Neutral    → Lo-fi / Chill
Surprised  → Energetic
```

*The exact emotion-to-genre mapping depends on the implementation.*

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Jinja2 Templates

### Backend

* Python
* Flask
* Gunicorn

### Machine Learning & Computer Vision

* CNN (Convolutional Neural Network)
* TensorFlow / Keras
* FER2013 Dataset
* OpenCV
* DeepFace

### Music Recommendation

* Spotify Web API
* Requests

### Other Libraries

* NumPy
* Pandas

### Development & Deployment

* Git
* GitHub
* Python `venv`
* Render

---

## 📁 Project Structure

```text
Moodrix/
│
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
│
├── templates/
│   └── ...
│
├── static/
│   ├── ...
│   └── assets/
│
├── model/
│   └── ...
│
└── README.md
```

> The exact structure may vary depending on the current version of the project.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Moodrix.git
cd Moodrix
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

If the project requires Spotify credentials, create a `.env` file or configure the required environment variables according to the current implementation.

**Do not upload API keys or secret credentials to GitHub.**

Example:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

---

### 5. Run the Application

Start the Flask application:

```bash
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

## 🎭 Emotion Detection

Moodrix uses facial-expression analysis to identify emotions from captured images.

The project uses the **FER2013 dataset**, which contains facial expressions categorized into multiple emotion classes.

The detected emotion is then passed to the recommendation layer.

```text
Facial Expression
       ↓
Emotion Classifier
       ↓
Emotion
       ↓
Genre Selection
       ↓
Music Recommendation
```

---

## 🎵 Spotify Integration

Moodrix uses the **Spotify Web API** to retrieve music-related information and generate recommendations based on the detected mood.

The application connects the detected emotion with suitable music categories before requesting relevant music data.

Spotify credentials should always be stored securely as environment variables.

---

## ☁️ Deployment

Moodrix is designed to be deployable as a Flask web application.

The repository includes deployment-related configuration such as:

```text
requirements.txt
Procfile
runtime.txt
```

The application can be deployed using platforms that support Python/Flask applications, such as **Render** or other compatible cloud platforms.

For production deployment, Gunicorn can be used as the WSGI server.

Example:

```bash
gunicorn app:app
```

---

## 🔐 Security

Never commit sensitive credentials to the repository.

Do **not** upload:

```text
.env
API keys
Spotify client secrets
private credentials
```

Add sensitive files to `.gitignore`.

---

## 📌 Current Status

### Completed

* [x] Flask web application
* [x] Web interface
* [x] Facial emotion detection
* [x] Computer vision integration
* [x] Emotion-based recommendation logic
* [x] Spotify API integration
* [x] Deployment configuration
* [x] GitHub repository setup

### Future Improvements

* [x] Improve emotion detection accuracy
* [ ] Improve recommendation personalization
* [ ] Add user accounts and personalized history
* [ ] Add more music platforms
* [ ] Improve UI/UX
* [x] Optimize model performance
* [ ] Add real-time playlist generation
* [ ] Improve mobile responsiveness

---

## 🎯 Project Goal

The goal of Moodrix is to make music discovery more **personal, interactive, and emotion-aware**.

Instead of manually selecting music based on how they feel, users can allow the system to detect their current facial expression and receive music recommendations accordingly.

---

## 👩‍💻 Project Type

**Academic / Machine Learning Project**

**Domain:**
Artificial Intelligence • Machine Learning • Computer Vision • Music Recommendation

---

## 📜 License

This project is intended for educational and academic purposes.

If a specific open-source license is added to the repository, update this section accordingly.

---

## ⭐ Acknowledgements

* **FER2013 Dataset** — facial expression recognition dataset
* **OpenCV** — computer vision functionality
* **DeepFace** — facial analysis
* **TensorFlow / Keras** — machine learning framework
* **Spotify Web API** — music data and recommendations
* **Flask** — Python web framework

