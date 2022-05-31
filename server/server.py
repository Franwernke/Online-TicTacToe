from socket import *
from repository import Repository
from exceptions.WrongPasswordException import WrongPasswordException
from exceptions.UserIsAlreadyInGame import UserIsAlreadyInGame
from log import Log

class Server:
  def __init__(self, repository: Repository, log: Log):
    self.repository = repository
    self.log = log

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
    userSession = self.repository.getOnlinePlayer(invitedUser)

    if userSession.availability == "emJogo":
      raise UserIsAlreadyInGame
    return userSession
  
  def logout(self, username):
    self.repository.removeOnlinePlayer(username)
  
  def handleHeartbeat(self, address):
    print(address, " está bem!")

  def startgame(self, invitingUser, invitedUser):
    self.repository.changeStatus(invitingUser, "emJogo")
    self.repository.changeStatus(invitedUser, "emJogo")

  def setWinner(self, winnerUser, loserUser):
    self.repository.changeStatus(winnerUser, "livre")
    self.repository.changeStatus(loserUser, "livre")

    score = self.repository.getUserScore(winnerUser)
    self.repository.changeUserScore(winnerUser, score + 3)

    firstIp = self.repository.getOnlinePlayer(winnerUser).ip

    secondIp = self.repository.getOnlinePlayer(loserUser).ip

    self.log.finishGame(winnerUser, loserUser, firstIp, secondIp, winnerUser)

  def drawGame(self, firstUser, secondUser):
    self.repository.changeStatus(firstUser, "livre")
    self.repository.changeStatus(secondUser, "livre")

    score = self.repository.getUserScore(firstUser)
    self.repository.changeUserScore(firstUser, score + 1)

    score = self.repository.getUserScore(secondUser)
    self.repository.changeUserScore(secondUser, score + 1)

    firstIp = self.repository.getOnlinePlayer(firstUser).ip

    secondIp = self.repository.getOnlinePlayer(secondUser).ip

    self.log.finishGame(firstUser, secondUser, firstIp, secondIp, "Ninguém")

  def endgame(self, firstUser, secondUser):
    self.repository.changeStatus(firstUser, "livre")
    self.repository.changeStatus(secondUser, "livre")

    firstIp = self.repository.getOnlinePlayer(firstUser).ip

    secondIp = self.repository.getOnlinePlayer(secondUser).ip

    self.log.finishGame(firstUser, secondUser, firstIp, secondIp, "Ninguém")


