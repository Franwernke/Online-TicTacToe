from socket import *
from repository import Repository
from exceptions.WrongPasswordException import WrongPasswordException

class Server:
  def __init__(self, repository: Repository):
    self.repository = repository

  def createNewUser(self, username, password):
    self.repository.createNewUser(username, password)

  def loginUser(self, username, password):
    user = self.repository.getUser(username)
    if user.password != password:
      raise WrongPasswordException()

  def changePassword(self, username, oldPassword, newPassword):
    user = self.repository.getUser(username)

    if user.password != oldPassword:
      raise WrongPasswordException()
    else:
      self.repository.changePassword(username, newPassword)


