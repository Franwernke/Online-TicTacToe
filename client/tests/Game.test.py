import sys
sys.path.insert(1, '/Users/franciscowernke/Documents/USP/Redes/Online-TicTacToe/client')

from Game import Game

game = Game("O")

game.markSpot("O", 0, 0)

game.markSpot("X", 0, 1)

game.markSpot("O", 0, 1)

game.markSpot("X", 2, 0)

game.printBoard()
