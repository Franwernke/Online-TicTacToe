#!/bin/python3

from clientStates import *
from socket import *

ENCODING = 'utf-8'

class Client:
  def __init__(self, controller, server) -> None:
    self.state = InitialState()
    self.controller = controller
    self.server = server

    self.server.acceptConnections()

  def changeState(self, newState):
    self.state = newState

  def createNewUser(self, user, password):
    self.state.createNewUser(self, user, password)

  def changeUserPassword(self, oldPassword, newPassword):
    self.state.changeUserPassword(self, oldPassword, newPassword)
  
  def loginUser(self, user, password, port):
    self.state.loginUser(self, user, password, port)
  
  def showHallOfFame(self):
    self.state.showHallOfFame(self)
  
  def showOnlinePlayers(self):
    self.state.showOnlinePlayers(self)

  def invitePlayer(self, opponent):
    print(self.state.invitePlayer(self, opponent))

  def sendMove(self, line, column):
    self.state.sendMove(self, line, column)

  def showLatency(self):
    self.state.showLatency(self)

  def endGame(self):
    self.state.endGame(self)

  def logout(self):
    self.state.logout(self)

  def sendMessage(self, message):
    return self.controller.sendMessage(message)
