import cv2
import pytesseract

# Global variables for rectangle coordinates
rect_x, rect_y, rect_width, rect_height = 500, 20, 800, 800

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

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1680)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1050)
    
    

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

        #cv2.rectangle(frame, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 255, 0), 2)
        # Display the frame on the screen
        cv2.imshow('Camera Stream', frame)

        # Check for key press
        key = cv2.waitKey(1)

        # Check for 'q' key press to quit
        if key & 0xFF == ord('q'):
            break
        # Check for 'c' key press to capture the content inside the rectangle
        elif key & 0xFF == ord('c'):

            cap.release()
            cv2.destroyAllWindows()

            #captured_image = frame[rect_y:rect_y + rect_height, rect_x:rect_x + rect_width]
            captured_image = frame

            select_roi(captured_image)

       

    # Release the VideoCapture object and close all OpenCV windows
    
    cv2.destroyAllWindows()




def select_roi(img):
    global start_x, start_y, end_x, end_y, drawing

    # Read the image
    #img = cv2.imread("testocr.jpg")

    # Create a window and set mouse callback to draw rectangle
    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', draw_rectangle)

    while True:
        # Display the image
        display_img = img.copy()

        # Draw the rectangle
        cv2.rectangle(display_img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        cv2.imshow('Image', display_img)

        # Check for key press to extract the region
        key = cv2.waitKey(1) & 0xFF
        if key == ord('e') and not drawing:
            # Extract the region within the rectangle
            selected_region = img[start_y:end_y, start_x:end_x]

            # Display the extracted region in a new window
            cv2.imshow('Selected Region', selected_region)
            

            text = pytesseract.image_to_string(selected_region,lang="fra")
            with open("ocr_result.txt",mode="w+") as f:
                f.write(text)

            #print(text)

        # Check for key press to exit the loop
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
