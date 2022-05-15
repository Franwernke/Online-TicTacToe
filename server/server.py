from socket import *
from repository import Repository

class Server:
  def __init__(self, repository: Repository):
    self.repository = repository

  def createNewUser(self, username, password):
    self.repository.createNewUser(username, password)