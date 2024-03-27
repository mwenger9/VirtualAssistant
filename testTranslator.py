# from translate import Translator


# translator = Translator(to_lang="fr",from_lang='autodetect')

# translation = translator.translate("你好，我的名字是罗伯特")

# print(translation)

import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Rennes\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
print(pytesseract.get_languages(config='.'))

# Set the language
language = 'rus'

# Open an image
image = Image.open('C:\\Users\\Rennes\\Desktop\\INSA\\VirtualAssistant\\russian-text.png')

# Perform OCR
text = pytesseract.image_to_string(image, lang=language)
print(text)