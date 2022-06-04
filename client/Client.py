#!/bin/python3
from threading import Thread, Lock
import time
from entities.ClientDomainI import ClientDomainI
from input.FeedbackController import FeedbackController, FifoChoice
from output.P2PRequester import P2PRequester
from output.Requester import Requester
from clientStates import State, LoggedIn, HisTurn, MyTurn
from socket import *

class ResponseTimeManager:
  def __init__(self, feedbackController: FeedbackController, timeoutLimit: int) -> None:
    self.receivedResponse = False
    self.feedbackController = feedbackController
    self.timeoutLimit = timeoutLimit

    self.timeCheckerThread = Thread(target=verifyResponseTimeThread, name="Response Time Checker Thread", args=[self])
    self.timeCheckerThread.daemon = True

  def verifyResponseTime(self):
    self.timeCheckerThread.start()

def verifyResponseTimeThread(responseTimeManager: ResponseTimeManager):
  tic = time.perf_counter()
  while True:
    delta = time.perf_counter() - tic
    if responseTimeManager.receivedResponse == True:
      return
    elif delta > responseTimeManager.timeoutLimit:
      responseTimeManager.feedbackController.sendResponse("reconnect", FifoChoice.serverResponse)
      return
    # elif delta > 5:
    #   responseTimeManager.feedbackController.sendResponse("", FifoChoice.serverResponse)
    time.sleep(1.2)


class LatencyRepository:
  def __init__(self) -> None:
    self.latency = []

  def startCounter(self):
    self.tic = time.perf_counter()

  def endCounter(self):
    delta = time.perf_counter() - self.tic
    self.latency.append(delta)

    if len(self.latency) > 3:
      del self.latency[0]

  def getLatency(self):
    return self.latency

  def resetLatency(self):
    self.latency = []


ENCODING = 'utf-8'

class ClientDomain(ClientDomainI):
  def __init__(self, serverOutput: Requester, peerToPeerOutput: P2PRequester, feedbackController: FeedbackController) -> None:
    self.user = None
    
    self.state = State.initialState(self)
    self.serverOutput = serverOutput
    self.peerToPeerOutput = peerToPeerOutput
    self.feedbackController = feedbackController

    self.latencyRepository = LatencyRepository()

    self.latencyLock = Lock()
    self.runLatencyThread = True
    self.measureLatency = False

    self.latencyThread = Thread(target=sendLatency, name="latency thread", args=[self])
    self.latencyThread.daemon = True
    self.latencyThread.start()

  def changeState(self, newState):
    if type(self.state) == LoggedIn and (type(newState) == HisTurn or type(newState) == MyTurn):
      self.latencyLock.acquire()
      self.measureLatency = True
      self.latencyLock.release()
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
    response = ""
    
    responseTimeManager = ResponseTimeManager(self.feedbackController, 180)
    responseTimeManager.verifyResponseTime()
    while not response:
      try:
        self.serverOutput.sendMessage(message)
      except Exception:
        pass
      response = self.feedbackController.recvResponse(FifoChoice.serverResponse)
    
    responseTimeManager.receivedResponse = True

    if response == "reconnect":
      try:
        self.serverOutput.transportLayer.restartConnection()
      except:
        print("Não foi possível reestabelecer a conexão com o servidor")
        print("Processo do servidor foi finalizado por um ‘kill -9")
        exit(1)

      self.tryToRecconect()

      return self.sendMessageToServer(message)

    return response
  
  def tryToRecconect(self):
    response = ""

    responseTimeManager = ResponseTimeManager(self.feedbackController, 10)
    responseTimeManager.verifyResponseTime()

    while not response:
      messageToSend = "reconnect"

      if self.user:
        messageToSend += " " + self.user

        if type(self.state) == LoggedIn:
          messageToSend += " " + "livre"
        else:
          messageToSend += " " + "emJogo"

        messageToSend += " " + str(self.peerToPeerOutput.getPort())

      self.serverOutput.sendMessage(messageToSend)
      response = self.feedbackController.recvResponse(FifoChoice.serverResponse)
    
    responseTimeManager.receivedResponse = True

    if response == "reconnect":
      print("Não foi possível reestabelecer a conexão com o servidor")
      print("Processo do servidor foi finalizado por um ‘kill -9")
      exit(1)
    


  def sendMessageToPeerToPeer(self, message):
    self.peerToPeerOutput.sendMessage(message)
    return self.feedbackController.recvResponse(FifoChoice.peerToPeerResponse)

  def sendMessageToPeerToPeerNoResp(self, message) -> str:
    self.peerToPeerOutput.sendMessage(message)

  def createConnectionWithClient(self, address, port):
    self.peerToPeerOutput.updateTransportLayer(address, port)

  def disconnectFromPlayer(self):

    self.latencyLock.acquire()
    self.measureLatency = False
    self.latencyRepository.resetLatency()
    self.latencyLock.release()

    self.peerToPeerOutput.killConnection()
  
  def answerLatency(self):
    self.sendMessageToPeerToPeerNoResp("P latency")

def sendLatency(client: ClientDomain):
  while client.runLatencyThread:
    client.latencyLock.acquire()

    if client.measureLatency:
      client.latencyRepository.startCounter()
      client.sendMessageToPeerToPeerNoResp("latency")
      client.feedbackController.recvResponse(FifoChoice.latency)
      client.latencyRepository.endCounter()

    client.latencyLock.release()
    time.sleep(1)

