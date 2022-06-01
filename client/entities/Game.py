from functools import reduce

class Directions:
  UP = -3
  DOWN = 3
  LEFT = -1
  RIGHT = 1
  UP_RIGHT = -2
  UP_LEFT = -4
  DOWN_RIGHT = 4
  DOWN_LEFT = 2
'''
[|0, 0, 0, |
  0, 1, 0, |
  0, 0, 0  |]
'''

class Game:
  def __init__(self, hisToken, opponentUser: str):
    self.board = [0 for i in range(9)]
    self.hisToken = hisToken
    self.myToken = "X" if self.hisToken == "O" else "O"
    self.opponentUser = opponentUser

  def printBoard(self):
    print("+---+---+---+")
    for i in range(len(self.board)):
      print("| ", end="")
      if self.board[i] == 0:
        print("  ", end="")
      else:
        print(self.board[i] + " ", end="")
      if i % 3 == 2:
        print("|\n+---+---+---+")

  def checkValidPlay(self, playX, playY):
    return playX < 3 and playY < 3 and self.board[playX + playY*3] == 0
  
  def markSpot(self, token, posX, posY):
    if self.checkValidPlay(posX, posY):
      self.board[posX + posY*3] = token

  def isDraw(self):
    return all(self.board)

  def didWin(self, token: str):
    allPossibleWins = []

    allPossibleWins.append(self.board[0:3:Directions.RIGHT])
    allPossibleWins.append(self.board[3:6:Directions.RIGHT])
    allPossibleWins.append(self.board[6:9:Directions.RIGHT])

    allPossibleWins.append(self.board[0:9:Directions.DOWN])
    allPossibleWins.append(self.board[1:9:Directions.DOWN])
    allPossibleWins.append(self.board[2:9:Directions.DOWN])

    allPossibleWins.append(self.board[0:9:Directions.DOWN_RIGHT])
    allPossibleWins.append(self.board[2:7:Directions.DOWN_LEFT])
    for win in allPossibleWins:
      if reduce(lambda acc, x: acc if x == token else False, win, True):
        return True
    return False
