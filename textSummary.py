import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QMimeData
from transformers import pipeline
from utils import *

class FileDragDropWidget(QWidget):
    
    
    
    def __init__(self):
        print("Initialisation scénario textSummarizer")
        super(FileDragDropWidget, self).__init__()

        self.summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")

        self.init_ui()

    def init_ui(self):
        # Set up the main layout
        layout = QVBoxLayout(self)
        self.label = QLabel('Drag and drop a file here', self)
        layout.addWidget(self.label)

        # Enable drag and drop events
        self.setAcceptDrops(True)

        self.setWindowTitle('Drag and Drop File')
        self.setGeometry(300, 300, 400, 200)

    def dragEnterEvent(self, event):
        # Accept only file drops
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) == 1:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        # Get the file path from the dropped URL
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.label.setText(f'Dropped File: {file_path}')
        print(f'Dropped File: {file_path}')

        with open(file_path, "r", encoding="utf-8") as file:
            text_content = file.read()

        summary = self.summarizer(text_content, max_length=1000, min_length=30, length_penalty=4.0, num_beams=4, early_stopping=True)


        self.label.setText(f'{summary[0]["summary_text"]}')
        #speak(summary[0]['summary_text'])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileDragDropWidget()
    window.show()
    sys.exit(app.exec_())
