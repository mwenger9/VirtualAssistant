import pytesseract


print(pytesseract.image_to_string("testocr.png",lang="eng"))

# import matplotlib.pyplot as plt
# import keras_ocr
# from pprint import pprint
# pipeline = keras_ocr.pipeline.Pipeline()


# images = [keras_ocr.tools.read("testocr.png")]

# prediction = pipeline.recognize(images)
# prediction = [e[0] for e in prediction[0]]
# pprint(prediction)