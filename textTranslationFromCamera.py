import cv2
import pytesseract
from translate import Translator
# Global variables for rectangle coordinates
rect_x, rect_y, rect_width, rect_height = 500, 20, 700, 300


def main():

    translator = Translator(to_lang="fr",from_lang='autodetect')


    # Pytesseract binary path 
    print("initialisation OCR")
    pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Rennes\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"




    global rect_x, rect_y, rect_width, rect_height

    # Create a VideoCapture object to capture video from the camera (0 is usually the default camera)
    print("starting video capture")
    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

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

        # text = pytesseract.image_to_string(frame[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width],lang="fra")
        # print(text)
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
            # print("analyzing text")
            text = pytesseract.image_to_string(captured_image,lang="rus")
            # print("done analyzing, display capture imaged..")cc
            cv2.imshow('Captured Image', captured_image)

            print(text)

            translation = translator.translate(text)
            print(translation)


            cv2.waitKey(0)  # Wait until any key is pressed to close the captured image window

    # Release the VideoCapture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
