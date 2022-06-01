#!/bin/python3

from entities.ClientDomainI import ClientDomainI
from input.FeedbackController import FeedbackController, FifoChoice
from output.P2PRequester import P2PRequester
from output.Requester import Requester
from clientStates import State
from socket import *

ENCODING = 'utf-8'

class ClientDomain(ClientDomainI):
  def __init__(self, serverOutput: Requester, peerToPeerOutput: P2PRequester, feedbackController: FeedbackController) -> None:
    self.state = State.initialState(self)
    self.serverOutput = serverOutput
    self.peerToPeerOutput = peerToPeerOutput
    self.feedbackController = feedbackController

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

  def receiveEndgame(self):
    self.state.receiveEndgame()

  def sendHeartbeat(self):
    self.serverOutput.sendMessage("heartbeat")

  def disconnect(self):
    self.serverOutput.sendMessage("bye")

  def sendMessageToServer(self, message):
    self.serverOutput.sendMessage(message)
    return self.feedbackController.recvResponse(FifoChoice.serverResponse)

  def sendMessageToPeerToPeer(self, message):
    self.peerToPeerOutput.sendMessage(message)
    return self.feedbackController.recvResponse(FifoChoice.peerToPeerResponse)

  def sendMessageToPeerToPeerNoResp(self, message) -> str:
    self.peerToPeerOutput.sendMessage(message)

  def createConnectionWithClient(self, address, port):
    self.peerToPeerOutput.updateTransportLayer(address, port)

  def disconnectFromPlayer(self):
    self.peerToPeerOutput.killConnection()
