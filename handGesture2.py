import cv2
import mediapipe as mp
import pyautogui



def scale_coordinates(hand_x, hand_y, cam_width, cam_height, screen_width, screen_height):
    """
    Scale and invert coordinates from camera resolution to screen resolution.

    Args:
    hand_x (float): X coordinate in camera space.
    hand_y (float): Y coordinate in camera space.
    cam_width (int): Width of the camera resolution.
    cam_height (int): Height of the camera resolution.
    screen_width (int): Width of the screen resolution.
    screen_height (int): Height of the screen resolution.

    Returns:
    (int, int): Tuple of scaled and mirrored coordinates (screen_x, screen_y).
    """
    # Calculate scale factors
    scale_x = screen_width / cam_width
    scale_y = screen_height / cam_height

    # Apply scale to convert camera coordinates to screen coordinates
    # Invert the x-axis by subtracting from cam_width
    screen_x = int((cam_width - hand_x) * scale_x)
    screen_y = int(hand_y * scale_y)

    return screen_x, screen_y


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Camera and screen resolutions
camera_width, camera_height = 1280, 720
screen_width, screen_height = pyautogui.size()

# Start capturing video
cap = cv2.VideoCapture(0)
cap.set(3, camera_width)  # Set the width
cap.set(4, camera_height)  # Set the height

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # Process the image and detect hands
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the wrist root as an example hand position
            wrist_root = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            hand_x = wrist_root.x * camera_width
            hand_y = wrist_root.y * camera_height

            # Scale coordinates
            screen_x, screen_y = scale_coordinates(hand_x, hand_y, camera_width, camera_height, screen_width, screen_height)

            # Move the cursor to the scaled coordinates
            pyautogui.moveTo(screen_x, screen_y)

    cv2.imshow('Frame', frame)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
