import serverStates

class server:
  def __init__(self) -> None:
    self.state = serverStates.initialState()
    pass

  def createNewUser(self):
    self.state.createNewUser()
  
  def loginUser(self):
    self.state.loginUser()

def main():
  input("JogoDaVelha>")

main()