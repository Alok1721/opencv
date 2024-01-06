import mediapipe as mp
import cv2
import numpy as np
import time
import win32api
import pyautogui
import threading

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Global variables for thread communication
index_finger_tip_coordinates = (0, 0)
mouse_down = False

def hand_tracking():
    global index_finger_tip_coordinates, mouse_down
    video = cv2.VideoCapture('http://192.168.137.135:4747/video')
    
    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
        while video.isOpened():
            _, frame = video.read()
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            image_height, image_width, _ = image.shape
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.multi_hand_landmarks:
                for num, hand in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2))
            
            if results.multi_hand_landmarks is not None:
                for hands_landmarks in results.multi_hand_landmarks:
                    for points in mp_hands.HandLandmark:
                        normalized_landmark = hands_landmarks.landmark[points]
                        pixel_coordinates_landmark = mp_drawing._normalized_to_pixel_coordinates(
                            normalized_landmark.x, normalized_landmark.y, image_width, image_height)
                        points = str(points)
                        
                        if points == 'HandLandmark.INDEX_FINGER_TIP':
                            try:
                                cv2.circle(image, (pixel_coordinates_landmark[0], pixel_coordinates_landmark[1]),
                                           25, (0, 0, 255), 5)
                                index_finger_tip_coordinates = (
                                    pixel_coordinates_landmark[0], pixel_coordinates_landmark[1])
                            except:
                                pass

            cv2.imshow('game', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()

def mouse_control():
    global index_finger_tip_coordinates, mouse_down
    while True:
        index_finger_tip_x, index_finger_tip_y = index_finger_tip_coordinates
        win32api.SetCursorPos((index_finger_tip_x*4, index_finger_tip_y*5))
        

        pyautogui.mouseDown(button='left' if mouse_down else 'right')
        time.sleep(0.05)  # Adjust sleep duration based on the desired frame rate

# Create threads for hand tracking and mouse control
hand_tracking_thread = threading.Thread(target=hand_tracking)
mouse_control_thread = threading.Thread(target=mouse_control)

# Start both threads
hand_tracking_thread.start()
mouse_control_thread.start()

# Wait for both threads to finish
hand_tracking_thread.join()
mouse_control_thread.join()
