import cv2
import mediapipe as mp
import pyautogui
import time
import os

# Suppress TensorFlow log messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Initialize webcam
cap = cv2.VideoCapture(0)

# Track dragging state
dragging = False

# Helper function to detect if a finger is up
def is_finger_up(lm, tip_id, pip_id, margin=0.02):
    return lm[tip_id].y < lm[pip_id].y - margin

# Detect if hand is open (for release)
def is_hand_open(lm):
    fingers = [
        is_finger_up(lm, 8, 6),   # Index
        is_finger_up(lm, 12, 10), # Middle
        is_finger_up(lm, 16, 14), # Ring
        is_finger_up(lm, 20, 18)  # Pinky
    ]
    return all(fingers)

# Main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm = handLms.landmark

            # Draw landmarks on webcam feed
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            # Get index finger tip position
            x = int(lm[8].x * screen_width)
            y = int(lm[8].y * screen_height)

            # Move cursor to index tip position
            pyautogui.moveTo(x, y)

            if is_hand_open(lm):
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False
                    cv2.putText(img, "Release", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
                    cv2.putText(img, "Dragging", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

    cv2.imshow("Angry Birds 2 Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
