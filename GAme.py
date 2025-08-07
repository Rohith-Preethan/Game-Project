import cv2
import mediapipe as mp
import pyautogui
import time
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

print("Switch to game window... Starting in 3 seconds.")
time.sleep(3)

def is_finger_up(lm, tip_id, pip_id, margin=0.02):
    return lm[tip_id].y < lm[pip_id].y - margin

def is_thumb_up(lm):
    return abs(lm[4].x - lm[3].x) > 0.05 and lm[4].x < lm[3].x

def classify_gesture(lm):
    thumb = is_thumb_up(lm)
    index = is_finger_up(lm, 8, 6)
    middle = is_finger_up(lm, 12, 10)
    ring = is_finger_up(lm, 16, 14)
    pinky = is_finger_up(lm, 20, 18)

    # Fist (all fingers down)
    if not (thumb or index or middle or ring or pinky):
        return "backward"
    # Victory sign (index + middle)
    elif index and middle and not (thumb or ring or pinky):
        return "left"
    # Index finger only
    elif index and not (thumb or middle or ring or pinky):
        return "right"
    # Rock on (index + pinky)
    elif index and pinky and not (thumb or middle or ring):
        return "jump"
    else:
        return "unknown"

def perform_action(gesture):
    pyautogui.keyUp("right")
    pyautogui.keyUp("left")
    pyautogui.keyUp("down")

    if gesture == "right":
        pyautogui.keyDown("right")
        print("Gesture: INDEX → RIGHT")
    elif gesture == "left":
        pyautogui.keyDown("left")
        print("Gesture: VICTORY → LEFT")
    elif gesture == "jump":
        pyautogui.press("space")
        print("Gesture: ROCK ON → JUMP")
    elif gesture == "backward":
        pyautogui.keyDown("down")
        print("Gesture: FIST → BACKWARD")

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture = "No hand"

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            lm = handLms.landmark
            gesture = classify_gesture(lm)
            perform_action(gesture)
    else:
        pyautogui.keyUp("right")
        pyautogui.keyUp("left")
        pyautogui.keyUp("down")

    cv2.putText(img, f"Gesture: {gesture}", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
