#!/bin/python3

from TransportLayer import TransportLayer
from FifoRouter import FifoRouter
from serverTCP import ServerTCP
from clientStates import State
from socket import *

ENCODING = 'utf-8'

class ClientDomain:
  def __init__(self, fifo) -> None:
    self.state = State.initialState(self)
    self.fifo: FifoRouter = fifo
    self.peerToPeerServer: ServerTCP = None
    self.serverController: TransportLayer = None

  def changeState(self, newState):
    self.state = newState

  def getState(self):
    return self.state

  def createNewUser(self, user, password):
    self.state.createNewUser(user, password)

  def changeUserPassword(self, oldPassword, newPassword):
    self.state.changeUserPassword(oldPassword, newPassword)
  
  def loginUser(self, user, password, port):
    self.state.loginUser(user, password, port)
  
  def showHallOfFame(self):
    self.state.showHallOfFame()
  
  def showOnlinePlayers(self):
    self.state.showOnlinePlayers()

  def invitePlayer(self, opponent):
    self.state.invitePlayer(opponent)

  def receiveInvite(self, opponent):
    self.state.receiveInvite(opponent)

  def sendMove(self, line, column):
    self.state.sendMove(line, column)

  def showLatency(self):
    self.state.showLatency()

  def endGame(self):
    self.state.endGame()

  def logout(self):
    self.state.logout()

  def acceptGame(self):
    self.state.acceptGame()

  def refuseGame(self):
    self.state.refuseGame()

  def sendMessage(self, message):
    self.serverController.sendMessage(message)
    return self.fifo.readCommand()
