from fer import FER
import cv2
import numpy as np
from collections import deque, Counter
from music import get_song

# --- Webcam ---
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# --- FER detector ---
detector = FER(mtcnn=False)

# --- Config ---
BUFFER_SIZE = 25
MIN_CONFIDENCE = 0.40
MIN_GAP = 0.10

EMOTIONS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

emotion_buffer = deque(maxlen=BUFFER_SIZE)
vote_buffer = deque(maxlen=10)

last_emotion = None


def get_smoothed_emotion(score_buf, vote_buf):
    if len(score_buf) < 8:
        return None, 0

    avg = {e: np.mean([f.get(e, 0) for f in score_buf]) for e in EMOTIONS}
    ranked = sorted(avg.items(), key=lambda x: x[1], reverse=True)

    top, top_score = ranked[0]
    second, sec_score = ranked[1]
    gap = top_score - sec_score

    if top_score < MIN_CONFIDENCE:
        return None, 0
    elif gap < MIN_GAP:
        final = 'neutral'
    elif (top, second) in [('angry', 'sad'), ('sad', 'angry')]:
        final = 'neutral'
    else:
        final = top

    vote_buf.append(final)
    majority = Counter(vote_buf).most_common(1)[0][0]

    return majority, top_score * 100


# --- Main loop ---
while True:
    ret, frame = cap.read()
    if not ret:
        break

    try:
        result = detector.detect_emotions(frame)
        if result:
            scores = result[0]['emotions']
            emotion_buffer.append(scores)
    except:
        pass

    emotion, confidence = get_smoothed_emotion(emotion_buffer, vote_buffer)

    # --- Song recommendation ---
    if emotion and emotion != last_emotion:
        song = get_song(emotion)
        print("\n🎧 New Recommendation:")
        print("Emotion   :", emotion)
        print("Confidence:", f"{confidence:.1f}%")
        print("Song      :", song["name"])
        print("Artist    :", song["artist"])
        print("Link      :", song["url"])
        last_emotion = emotion

    # --- Display ---
    label = f"{emotion} ({confidence:.1f}%)" if emotion else "Detecting..."
    cv2.putText(frame, label, (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

    cv2.imshow("Moodrix 💜", frame)

    # ✅ EXIT CONTROL (FIXED)
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break


# ✅ CLEAN EXIT (VERY IMPORTANT)
cap.release()
cv2.destroyAllWindows()