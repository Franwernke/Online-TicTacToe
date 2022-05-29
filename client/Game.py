class Directions:
  UP = -3
  DOWN = 3
  LEFT = -1
  RIGHT = 1
  UP_RIGHT = -2
  UP_LEFT = -4
  DOWN_RIGHT = 4
  DOWN_LEFT = 2

class Game:
  def __init__(self, hisToken):
    self.board = [0 for i in range(9)]
    self.hisToken = hisToken
    self.myToken = "X" if self.hisToken == "O" else "O"

  def printBoard(self):
    print("+---+---+---+")
    for i in range(len(self.board)):
      print("| ", end="")
      if self.board[i] == 0:
        print("  ", end="")
      elif self.board[i] == 1:
        print("X ", end="")
      else:
        print("O ", end="") 
      if i % 3 == 2:
        print("|\n+---+---+---+")

  def checkValidPlay(self, playX, playY):
    return playX < 3 and playY < 3 and self.board[playX + playY*3] == 0
  
  def markSpot(self, token, posX, posY):
    if self.checkValidPlay(posX, posY):
      self.board[posX + posY*3] = 1 if token == "X" else "O"

  def didHeWin(self, playX, playY):
    curPosX = playX
    curPosY = playY

    # check vertical
    # while curPosX < 3 and curPosY < 3:
    #   if self.board[curPosX + 3*curPosY] == self.myToken:
    #     return False
    #   if curPosX + Directions.UP[0] < 3:
        