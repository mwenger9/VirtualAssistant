import cv2

# Global variables for rectangle coordinates and state
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
            cv2.waitKey(0)  # Wait until any key is pressed to close the window

        # Check for key press to exit the loop
        elif key == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    img = cv2.imread("testocr.jpg")
    select_roi(img)
