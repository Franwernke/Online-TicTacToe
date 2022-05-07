import clientStates

class client:
  def __init__(self) -> None:
    self.state = clientStates.initialState()
    pass

  def createNewUser(self):
    self.state.createNewUser()
  
  def loginUser(self):
    self.state.loginUser()

def main():
  input("JogoDaVelha>")

main()