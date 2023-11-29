import chess
import chess.svg
from stockfish import Stockfish
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget
from utils import *
from time import sleep
class MainWindow(QWidget):
    def __init__(self,user_color="white"):
        super().__init__()
        self.user_color = user_color
        self.setGeometry(100, 100, 550, 550)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 500, 500)

        self.chessboard = chess.Board()
        self.engine = Stockfish("models\stockfish\stockfish-windows-x86-64-avx2.exe")
        self.engine.set_depth(20) # Va de 2 à 20 (20 = le plus fort)

        self.update_chessboard()

    def make_move(self, move_str):
        try :
            move = chess.Move.from_uci(move_str)
        except:
            print(f"Invalid move: {move_str}")
            return False
        if move in self.chessboard.legal_moves:
            self.chessboard.push(move)
            self.update_chessboard()
            return True
        else:
            print(f"Illegal move: {move_str}")
            return False

    def update_chessboard(self):
        flipped = self.user_color == "black"
        self.chessboardSvg = chess.svg.board(self.chessboard,flipped=flipped).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def get_opponent_move(self):
        self.engine.set_fen_position(self.chessboard.fen())
        result = self.engine.get_best_move()
        return result

if __name__ == "__main__":
    app = QApplication([])
    
    
    # Ask the user for their preferred color
    speak("Choisissez votre couleur, blanc ou noir ?")
    user_color = listen_once().lower()
    user_color = "white" if "blanc" in user_color else "black" if "noir" in user_color else ""

    if user_color not in ['white', 'black']:
        print(f"Couleur non trouvée")
        user_color = "white"
    window = MainWindow(user_color)
    # Set the board orientation based on the user's choice
    if user_color == 'black':
        window.chessboard = window.chessboard.mirror()

    window.show()
    speak("Donnez un coup à jouer à voix haute sous la forme case de départ case d'arrivée ou dites stop pour mettre fin à la partie")

    
    move = listen_once().lower().replace(" ","")
    window.make_move(move)

    

    # while not window.chessboard.is_game_over():
    #     print("Donnez un coup à jouer ou dites stop pour mettre fin à la partie")
    #     move = listen_once().lower().replace(" ","") # Add parsing logic to find the actual move, may not work like this
        

    #     if move.lower() == 'stop':
    #         exit()
        
    #     is_legal_move = window.make_move(move)
    #     while(not is_legal_move):
    #         print("Donnez un coup à jouer ou dites stop pour mettre fin à la partie")
    #         move = listen_once()
    #         if(not move):
    #             continue
    #         move = move.lower().replace(" ","")
    #         is_legal_move = window.make_move(move)
    #     print()

    #     opponent_move = window.get_opponent_move()
    #     window.make_move(opponent_move)
    #     print()


    app.exec()