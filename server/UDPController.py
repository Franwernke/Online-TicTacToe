from socket import *
import sys
from threading import Thread, Lock
import time
from server import Server
from GenericController import GenericController
from log import Log

class UDPSocketWrapper:
  def __init__(self, address: tuple) -> None:
    self.address = address
    self.keepHeartbeating = True
    self.lock = Lock()
    self.receivedResponse = False

  def getResponseOrFail(self):
    tic = time.perf_counter()
    while True:
      delta = time.perf_counter() - tic
      if self.receivedResponse == True:
        self.receivedResponse = False
        print("Recebi a resposta do heartbeat de", self.address)
        print("Resposta em", delta, "segundos")
        return True
      elif delta > 5:
        print("TIMEOUT: O cliente", self.address, "foi desconectado")
        return False

class UDPController(GenericController):
  def __init__(self, port, server: Server, log: Log):
    self.server = server
    self.log = log

    self.listenfd = socket(AF_INET, SOCK_DGRAM)
    self.listenfd.bind((str(INADDR_ANY), port))
    self.wrappers = dict()
    self.disconnected = dict()
    self.acceptConnectionsThread = Thread(target=acceptConnectionsThreadFunc, name='Accept connections thread', args=[self])
    self.acceptConnectionsThread.daemon = True


  def acceptConnections(self):
    self.acceptConnectionsThread.start()

  def sendMessage(self, messageStr: str, address):
    message = bytes(messageStr, "utf-8")
    self.listenfd.sendto(message, address)

  def resolveMessage(self, message: str, address):
    command = message.split()
    # self.writeInFifo()
    responseString = self.processCommand(command, address)

    if responseString != "DONOTANSWER":
      self.sendMessage(responseString, address)

def acceptConnectionsThreadFunc(controller: UDPController):
  
  while True:
    recvline = controller.listenfd.recvfrom(4096)

    if not recvline[1] in controller.wrappers:
      
      controller.log.newConnection(recvline[1][0])

      socketWrapperForHeartbeats = UDPSocketWrapper(recvline[1])

      controller.wrappers[recvline[1]] = socketWrapperForHeartbeats
      controller.disconnected[recvline[1]] = False

      sendHeartbeatsThread = Thread(target=sendHeartbeats, name='Address ' + str(recvline[1]) + ' heartbeat', 
                                    args=[controller, socketWrapperForHeartbeats])
      sendHeartbeatsThread.daemon = True
      sendHeartbeatsThread.start()

    message = recvline[0].decode("utf-8")
    if message == 'heartbeat':
      controller.wrappers[recvline[1]].receivedResponse = True
    else:
      if message == 'bye':
        controller.disconnected[recvline[1]] = True
      controller.resolveMessage(recvline[0].decode("utf-8"), recvline[1])
    
    print("Received from UDP: " + recvline[0].decode("utf-8"))
    sys.stdout.flush()

def sendHeartbeats(controller: UDPController, socketWrapper: UDPSocketWrapper):
  while socketWrapper.keepHeartbeating:
    controller.delayHeartbeat()
    controller.sendMessage("heartbeat", socketWrapper.address)
    print("Mandei um heartbeat para ", socketWrapper.address)
    if not socketWrapper.getResponseOrFail():
      controller.server.disconnectDueToTimeout(socketWrapper.address)
      socketWrapper.keepHeartbeating = False

      if controller.disconnected[socketWrapper.address]:
        print("O cliente foi desconectado!")
      else:
        print("Desconexão inesperada do cliente!")
        controller.log.unexpectedDisconnect(socketWrapper.address[0])