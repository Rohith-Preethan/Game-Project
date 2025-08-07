import cv2
import mediapipe as mp
import numpy as np

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Finger tip landmark indices
FINGER_TIPS = [8, 12, 16, 20]
THUMB_TIP = 4

# Check if a finger is up
def fingers_up(hand):
    fingers = []
    lm = hand.landmark
    # Thumb
    fingers.append(lm[THUMB_TIP].x < lm[THUMB_TIP - 1].x)
    # Other fingers
    for tip in FINGER_TIPS:
        fingers.append(lm[tip].y < lm[tip - 2].y)
    return fingers

# Webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            lm = hand.landmark
            up = fingers_up(hand)

            # Landmarks for fingers
            cx0, cy0 = int(lm[0].x * w), int(lm[0].y * h)       # palm center
            cx8, cy8 = int(lm[8].x * w), int(lm[8].y * h)       # index tip
            cx12, cy12 = int(lm[12].x * w), int(lm[12].y * h)   # middle tip

            # ===============================
            # 🔥 Fireball: All fingers up
            # ===============================
            if up == [True, True, True, True, True]:
                overlay = img.copy()
                for r, c, a in [
                    (60, (0, 255, 255), 0.2),
                    (40, (0, 180, 255), 0.3),
                    (25, (0, 100, 255), 0.5),
                    (10, (0, 0, 255), 1.0)
                ]:
                    temp = overlay.copy()
                    cv2.circle(temp, (cx0, cy0), r, c, -1)
                    overlay = cv2.addWeighted(temp, a, overlay, 1 - a, 0)
                img = overlay

            # ===============================
            # 🔫 Lasers: Index & Middle up
            # ===============================
            elif up[1] and up[2] and not any(up[i] for i in [0, 3, 4]):
                cv2.line(img, (cx8, cy8), (cx8, cy8 - 200), (255, 0, 0), 5)
                cv2.line(img, (cx12, cy12), (cx12, cy12 - 200), (0, 0, 255), 5)

            # ===============================
            # 💡 Light Trail: Only Index up
            # ===============================
            elif up == [False, True, False, False, False]:
                cv2.circle(img, (cx8, cy8), 20, (0, 255, 0), -1)
                cv2.circle(img, (cx8, cy8), 40, (0, 255, 0), 2)

            # ===============================
            # 😎 Emoji Effect: Fist (all down)
            # ===============================
            elif up == [False, False, False, False, False]:
                cv2.putText(img, "😎", (cx0 - 20, cy0), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)

            # Draw landmarks
            mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

    # Show image
    cv2.imshow("AR Hand Effects", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
