# import pyautogui
# import time

# # Wait for 3 seconds to switch to your game window
# time.sleep(3)

# # Press the keys one by one
# pyautogui.press('space')  # Test jump
# time.sleep(1)
# pyautogui.press('down')  # Test down
# time.sleep(1)
# pyautogui.press('right')  # Test right
# time.sleep(1)
# pyautogui.press('left')  # Test left
 

#  # # import cv2
# # # import mediapipe as mp
# # # from pynput.keyboard import Key, Controller
# # # import time
# # # import math
# # # import os

# # # # OPTIONAL: Suppress TensorFlow/MediaPipe logs
# # # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# # # # MediaPipe hands setup
# # # mp_hands = mp.solutions.hands
# # # hands = mp_hands.Hands(static_image_mode=False,
# # #                        max_num_hands=1,
# # #                        min_detection_confidence=0.7,
# # #                        min_tracking_confidence=0.5)
# # # mp_draw = mp.solutions.drawing_utils

# # # # Keyboard controller
# # # keyboard = Controller()

# # # # Utility functions
# # # def get_finger_states(landmarks):
# # #     tips_ids = [4, 8, 12, 16, 20]
# # #     states = []
# # #     for i, tip_id in enumerate(tips_ids):
# # #         tip = landmarks[tip_id]
# # #         pip = landmarks[tip_id - 2]
# # #         states.append(tip.y < pip.y)
# # #     return states

# # # def classify_gesture(finger_states):
# # #     if finger_states == [False, True, False, False, False]:
# # #         return "left"
# # #     elif finger_states == [False, True, True, False, False]:
# # #         return "right"
# # #     elif all(finger_states):
# # #         return "open"
# # #     elif not any(finger_states):
# # #         return "fist"
# # #     elif finger_states[0] and not any(finger_states[1:]):
# # #         return "thumbs_up"
# # #     else:
# # #         return "unknown"

# # # def perform_action(gesture):
# # #     if gesture == "open":
# # #         keyboard.press(Key.up)
# # #         print("Gesture: OPEN → UP")
# # #     elif gesture == "fist":
# # #         keyboard.press(Key.down)
# # #         print("Gesture: FIST → DOWN")
# # #     elif gesture == "thumbs_up":
# # #         keyboard.press(Key.space)
# # #         time.sleep(0.2)
# # #         keyboard.release(Key.space)
# # #         print("Gesture: THUMBS UP → SPACE")
# # #     elif gesture == "left":
# # #         keyboard.press(Key.left)
# # #         print("Gesture: INDEX → LEFT")
# # #     elif gesture == "right":
# # #         keyboard.press(Key.right)
# # #         print("Gesture: INDEX+MIDDLE → RIGHT")
# # #     else:
# # #         keyboard.release(Key.up)
# # #         keyboard.release(Key.down)
# # #         keyboard.release(Key.left)
# # #         keyboard.release(Key.right)

# # # # Main loop
# # # cap = cv2.VideoCapture(0)
# # # while True:
# # #     success, frame = cap.read()
# # #     if not success:
# # #         break

# # #     frame = cv2.flip(frame, 1)
# # #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# # #     result = hands.process(rgb)

# # #     if result.multi_hand_landmarks:
# # #         for handLms in result.multi_hand_landmarks:
# # #             mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
# # #             finger_states = get_finger_states(handLms.landmark)
# # #             gesture = classify_gesture(finger_states)
# # #             perform_action(gesture)
# # #     else:
# # #         # Release all keys if no hand detected
# # #         keyboard.release(Key.up)
# # #         keyboard.release(Key.down)
# # #         keyboard.release(Key.left)
# # #         keyboard.release(Key.right)

# # #     cv2.imshow("Hand Gesture Controller", frame)
# # #     if cv2.waitKey(1) & 0xFF == ord('q'):
# # #         break

# # # cap.release()
# # # cv2.destroyAllWindows()

# # #-----------------------------------------------------------------------------------------------------------------------------------------------------

# # import cv2
# # import mediapipe as mp
# # from pynput.keyboard import Key, Controller
# # import time
# # import os

# # # Suppress TensorFlow warnings
# # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# # # Initialize MediaPipe and keyboard
# # mp_hands = mp.solutions.hands
# # hands = mp_hands.Hands(static_image_mode=False,
# #                        max_num_hands=1,
# #                        min_detection_confidence=0.7,
# #                        min_tracking_confidence=0.5)
# # mp_draw = mp.solutions.drawing_utils
# # keyboard = Controller()

# # # Determine which fingers are up
# # def get_finger_states(landmarks):
# #     tips_ids = [4, 8, 12, 16, 20]
# #     states = []
# #     for i, tip_id in enumerate(tips_ids):
# #         tip = landmarks[tip_id]
# #         pip = landmarks[tip_id - 2]
# #         states.append(tip.y < pip.y)  # True = finger up
# #     return states  # [Thumb, Index, Middle, Ring, Pinky]

# # # Recognize gesture from finger states
# # def classify_gesture(finger_states):
# #     thumb, index, middle, ring, pinky = finger_states
# #     if all(finger_states):
# #         return "jump"
# #     elif not any(finger_states):
# #         return "backward"
# #     elif thumb and not (index or middle or ring or pinky):
# #         return "right"
# #     elif middle and not (thumb or index or ring or pinky):
# #         return "left"
# #     else:
# #         return "unknown"

# # # Perform key actions
# # def perform_action(gesture):
# #     if gesture == "jump":
# #         keyboard.press(Key.space)
# #         print("Gesture: OPEN → JUMP")
# #         time.sleep(0.2)
# #         keyboard.release(Key.space)
# #     elif gesture == "backward":
# #         keyboard.press(Key.down)
# #         print("Gesture: FIST → BACKWARD")
# #     elif gesture == "right":
# #         keyboard.press(Key.right)
# #         print("Gesture: THUMB → RIGHT")
# #     elif gesture == "left":
# #         keyboard.press(Key.left)
# #         print("Gesture: MIDDLE → LEFT")
# #     else:
# #         # Release keys when gesture is unrecognized
# #         keyboard.release(Key.down)
# #         keyboard.release(Key.left)
# #         keyboard.release(Key.right)

# # # Webcam + gesture loop
# # cap = cv2.VideoCapture(0)
# # while True:
# #     success, frame = cap.read()
# #     if not success:
# #         break

# #     frame = cv2.flip(frame, 1)
# #     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #     results = hands.process(rgb)

# #     if results.multi_hand_landmarks:
# #         for handLms in results.multi_hand_landmarks:
# #             mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
# #             states = get_finger_states(handLms.landmark)
# #             gesture = classify_gesture(states)
# #             perform_action(gesture)
# #     else:
# #         # Release all keys if no hand
# #         keyboard.release(Key.down)
# #         keyboard.release(Key.left)
# #         keyboard.release(Key.right)

# #     cv2.imshow("Hand Gesture Controller", frame)
# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #         break

# # cap.release()
# # cv2.destroyAllWindows()

# #---------------------------------------------------------------------------------------------------------------------------------------

# import cv2
# import mediapipe as mp
# import pyautogui
# import time
# import os

# # Suppress TensorFlow warnings
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# # Initialize MediaPipe and keyboard
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(static_image_mode=False,
#                        max_num_hands=1,
#                        min_detection_confidence=0.7,
#                        min_tracking_confidence=0.5)
# mp_draw = mp.solutions.drawing_utils

# # Determine which fingers are up
# def get_finger_states(landmarks):
#     tips_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
#     states = []
#     for i, tip_id in enumerate(tips_ids):
#         tip = landmarks[tip_id]
#         pip = landmarks[tip_id - 2]
#         states.append(tip.y < pip.y)  # True = finger up
#     return states  # [Thumb, Index, Middle, Ring, Pinky]

# # Recognize gesture from finger states
# def classify_gesture(finger_states):
#     thumb, index, middle, ring, pinky = finger_states
#     if all(finger_states):
#         return "jump"  # All fingers up for jump
#     elif not any(finger_states):
#         return "down"  # Fist for down
#     elif thumb and not (index or middle or ring or pinky):
#         return "right"  # Thumb up for right
#     elif middle and not (thumb or index or ring or pinky):
#         return "left"  # Middle finger for left
#     else:
#         return "unknown"  # Unknown gesture

# # Perform key actions
# def perform_action(gesture):
#     if gesture == "jump":
#         pyautogui.press("space")
#         print("Gesture: OPEN → JUMP")
#     elif gesture == "down":
#         pyautogui.keyDown("down")
#         print("Gesture: FIST → DOWN")
#     elif gesture == "right":
#         pyautogui.keyDown("right")
#         print("Gesture: THUMB → RIGHT")
#     elif gesture == "left":
#         pyautogui.keyDown("left")
#         print("Gesture: MIDDLE → LEFT")
#     else:
#         # Release all keys if no recognized gesture
#         pyautogui.keyUp("down")
#         pyautogui.keyUp("left")
#         pyautogui.keyUp("right")

# # Webcam + gesture loop
# cap = cv2.VideoCapture(0)
# while True:
#     success, frame = cap.read()
#     if not success:
#         break

#     frame = cv2.flip(frame, 1)  # Flip to make it a mirror view
#     rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = hands.process(rgb)

#     if results.multi_hand_landmarks:
#         for handLms in results.multi_hand_landmarks:
#             mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
#             states = get_finger_states(handLms.landmark)
#             gesture = classify_gesture(states)
#             perform_action(gesture)
#     else:
#         # Release all keys if no hand detected
#         pyautogui.keyUp("down")
#         pyautogui.keyUp("left")
#         pyautogui.keyUp("right")

#     cv2.imshow("Hand Gesture Controller", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
