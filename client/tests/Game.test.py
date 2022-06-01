import sys
sys.path.insert(1, '/Users/franciscowernke/Documents/USP/Redes/Online-TicTacToe/client')

from entities.Game import Game

game = Game("O", "joao")

print("começo")

game.markSpot("X", 0, 0)
game.markSpot("X", 1, 1)
game.markSpot("X", 2, 1)

game.printBoard()

print(game.didWin("X"))
