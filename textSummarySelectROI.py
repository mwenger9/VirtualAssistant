import cv2
import pytesseract

# Global variables for rectangle coordinates
rect_x, rect_y, rect_width, rect_height = 500, 20, 700, 600

start_x, start_y = -1, -1
end_x, end_y = -1, -1
drawing = False

def draw_rectangle(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        end_x, end_y = x, y
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            end_x, end_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


def main():


    # Pytesseract binary path 
    pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Rennes\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"




    global rect_x, rect_y, rect_width, rect_height, drawing

    # Create a VideoCapture object to capture video from the camera (0 is usually the default camera)
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



            captured_image = frame[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]


            cv2.imshow('Captured Image', captured_image)
            cv2.namedWindow('Captured Image')
            cv2.setMouseCallback('Captured Image', draw_rectangle)

           
            # text = pytesseract.image_to_string(captured_image,lang="fra")
            

            selected_roi = None

            while True:
                key2 = cv2.waitKey(1) & 0xFF
                if key2 == ord('e') and not drawing:
                    # Extract the region within the rectangle
                    selected_roi = captured_image[start_y:end_y, start_x:end_x]
                    break
                elif key2 == ord('q'):
                    break

            if selected_roi is not None:
                # Draw the rectangle highlighting the selected ROI
                cv2.rectangle(captured_image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
                cv2.imshow('Captured Image', captured_image)


       

    # Release the VideoCapture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
