import cv2

# Global variables for rectangle coordinates
rect_x, rect_y, rect_width, rect_height = 20, 20, 300, 300

def main():
    global rect_x, rect_y, rect_width, rect_height

    # Create a VideoCapture object to capture video from the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Loop to continuously read frames from the camera
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            print("Error: Could not read frame.")
            break

        # Draw a green rectangle on the frame
        cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 2)

        # Display the frame on the screen
        cv2.imshow('Camera Stream', frame)

        # Check for key press
        key = cv2.waitKey(1)

        # Check for 'q' key press to quit
        if key & 0xFF == ord('q'):
            break
        # Check for 'c' key press to capture the content inside the rectangle
        elif key & 0xFF == ord('c'):
            # Capture the content inside the rectangle
            captured_image = frame[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]
            # Show the captured image in a new window
            cv2.imshow('Captured Image', captured_image)
            cv2.waitKey(0)  # Wait until any key is pressed to close the captured image window

    # Release the VideoCapture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
