import chess
import chess.svg
from stockfish import Stockfish
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QThread, pyqtSignal,QTimer
from utils import *

class SpeakThread(QThread):
    finished = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.text = text

    def run(self):
        speak(self.text)
        self.finished.emit()

class ListenThread(QThread):
    finished = pyqtSignal(str)

    def run(self):
        result = listen_once()
        if not result : 
            return
        self.finished.emit(result.lower().replace(" ", ""))

class MainWindow(QWidget):
    def __init__(self, user_color="white"):
        super().__init__()
        self.user_color = user_color
        self.setGeometry(100, 100, 550, 550)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 500, 500)

        self.chessboard = chess.Board()
        self.engine = Stockfish("models\stockfish\stockfish-windows-x86-64-avx2.exe")
        self.engine.set_depth(20)

        self.update_chessboard()

        # Add a button for testing purposes
        self.test_button = QPushButton("Donner un coup")
        self.test_button.clicked.connect(self.start_sequence)
        layout = QVBoxLayout(self)
        layout.addWidget(self.widgetSvg)
        layout.addWidget(self.test_button)

        # Store the threads as instance variables
        self.speak_thread = None
        self.listen_thread = None

    def start_sequence(self):
        # Check if threads are running and finish them if necessary

        if self.listen_thread and self.listen_thread.isRunning():
            self.listen_thread.quit()
            self.listen_thread.wait()

        # Create new threads
        self.listen_thread = ListenThread()

        # Connect signals and slots
        self.listen_thread.finished.connect(self.handle_listen_result)

        self.listen_thread.start()

    def handle_listen_result(self, result):
        print(f"Received result: {result}")
        res = self.make_move(result)
        if not res:
            return

        self.update_chessboard()

        # Create a QTimer
        timer = QTimer(self)
        timer.setSingleShot(True)  # Set to single shot mode
        timer.timeout.connect(self.delayed_opponent_move)
        
        # Start the timer with a 2-second interval
        timer.start(1000)



    def delayed_opponent_move(self):
        self.make_move(self.get_opponent_move())
        self.update_chessboard()

        

    def get_opponent_move(self):
        self.engine.set_fen_position(self.chessboard.fen())
        result = self.engine.get_best_move()
        return result


    def make_move(self, move_str):
        try:
            move = chess.Move.from_uci(move_str)
        except ValueError:
            print(f"Invalid move: {move_str}")
            return False

        if move in self.chessboard.legal_moves:
            self.chessboard.push(move)
            self.update_chessboard()
            print(f"Move made: {move}")
            return True
        else:
            print(f"Illegal move: {move_str}")
            return False

    def update_chessboard(self):
        flipped = self.user_color == "black"
        self.chessboardSvg = chess.svg.board(self.chessboard, flipped=flipped).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
