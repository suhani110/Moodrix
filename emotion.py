from deepface import DeepFace
import cv2
from music import get_song   # 👈 import your music function

cap = cv2.VideoCapture(0)

last_emotion = None  # to avoid repeating

while True:
    ret, frame = cap.read()

    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

    emotion = result[0]['dominant_emotion']
    confidence = result[0]['emotion'][emotion]

    # Only fetch new song if emotion changes
    if emotion != last_emotion:
        song = get_song(emotion)
        print("\n🎧 New Recommendation:")
        print("Emotion:", emotion)
        print("Song:", song["name"])
        print("Artist:", song["artist"])
        print("Link:", song["url"])
        last_emotion = emotion

    # Display on screen
    cv2.putText(frame, f"{emotion} ({confidence:.1f}%)",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 255), 2)

    cv2.imshow("Moodrix 💜", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()