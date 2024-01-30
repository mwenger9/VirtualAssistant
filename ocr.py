import pytesseract
import cv2

img = cv2.imread("testocr.jpg")
#C:\Users\Rennes\AppData\Local\Programs\Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Rennes\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"


text = pytesseract.image_to_string(img,lang="fra")

print(text)