import pickle
import pyautogui
import cv2
import mediapipe as mp
import numpy as np



def scale_coordinates(hand_x, hand_y, cam_width, cam_height, screen_width, screen_height):
    # Calculate scale factors
    scale_x = screen_width / cam_width
    scale_y = screen_height / cam_height

    # Apply scale to convert camera coordinates to screen coordinates
    # Invert the x-axis by subtracting from cam_width
    screen_x = int((cam_width - hand_x) * scale_x)
    screen_y = int(hand_y * scale_y)

    return screen_x, screen_y



model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']
camera_width, camera_height = 1280, 720
screen_width, screen_height = pyautogui.size()

cap = cv2.VideoCapture(0)

cap.set(3, camera_width)  # Set the width
cap.set(4, camera_height)  # Set the height

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3,max_num_hands=1)

labels_dict = {0: 'Open', 1: 'Closed'}


mouse_pressed = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            wrist_root = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            hand_x = wrist_root.x * camera_width
            hand_y = wrist_root.y * camera_height

            screen_x, screen_y = scale_coordinates(hand_x, hand_y, camera_width, camera_height, screen_width, screen_height)
            pyautogui.moveTo(screen_x, screen_y)

            # Collect data for prediction
            data_aux = []
            x_ = [landmark.x for landmark in hand_landmarks.landmark]
            y_ = [landmark.y for landmark in hand_landmarks.landmark]

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        # Make a prediction
        prediction = model.predict([np.asarray(data_aux)])
        predicted_character = labels_dict[int(prediction[0])]

        if predicted_character == 'Closed' and not mouse_pressed:
            pyautogui.mouseDown()
            mouse_pressed = True
        elif predicted_character == 'Open' and mouse_pressed:
            pyautogui.mouseUp()
            mouse_pressed = False

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()