class ClientDomainI:
  def __init__(self, serverOutput, peerToPeerOutput, feedbackController) -> None:
    pass

  def changeState(self, newState):
    pass

  def getState(self):
    pass

  def createNewUser(self, user, password):
    pass

  def changeUserPassword(self, oldPassword, newPassword):
    pass
  
  def loginUser(self, user, password, port):
    pass
  
  def showHallOfFame(self):
    pass
  
  def showOnlinePlayers(self):
    pass

  def invitePlayer(self, opponent):
    pass

  def receiveInvite(self, opponent):
    pass

  def sendMove(self, line, column):
    pass

  def showLatency(self):
    pass

  def endGame(self):
    pass

  def logout(self):
    pass

  def acceptGame(self):
    pass

  def refuseGame(self):
    pass

  def sendMessageToServer(self, message) -> str:
    pass

  def sendMessageToPeerToPeer(self, message) -> str:
    pass
  
  def sendMessageToPeerToPeerNoResp(self, message) -> str:
    pass
  
  def createConnectionWithClient(self, address, port):
    pass
