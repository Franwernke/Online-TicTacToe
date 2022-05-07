class clientStates:
  def __init__(self) -> None:
    self.clientPort = 0
  
  def createNewUser(self, A, B):
    pass


class initialState(clientStates):
  def createNewUser(self, A, B):
    A = 2
    B = 3
    return A + B

