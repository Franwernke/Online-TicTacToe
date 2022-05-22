from socket import *
from repository import Repository
from exceptions.WrongPasswordException import WrongPasswordException

class Server:
  def __init__(self, repository: Repository):
    self.repository = repository

  def createNewUser(self, username, password):
    self.repository.createNewUser(username, password)
    self.repository.changeUserScore(username, 0)

  def loginUser(self, username, password, address):
    user = self.repository.getUser(username)
    if user.password != password:
      raise WrongPasswordException()
    self.repository.createOnlinePlayer(username, address)


  def changePassword(self, username, oldPassword, newPassword):
    user = self.repository.getUser(username)

    if user.password != oldPassword:
      raise WrongPasswordException()
    else:
      self.repository.changePassword(username, newPassword)

  def showHallOfFame(self):
    return sorted(self.repository.getScores().items(), key=lambda score: score[1], reverse=True)
  
  def showOnlinePlayers(self):
    return self.repository.listOnlinePlayers()

  def invitePlayer(self, invitingUser, invitedUser):
    try:
      self.repository.getOnlinePlayer()
    except:
      pass
  
  def logout(self, username):
    self.repository.removeOnlinePlayer(username)
  
  def handleHeartbeat(self, address):
    print(address, " está bem!")


