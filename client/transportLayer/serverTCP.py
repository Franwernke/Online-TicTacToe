from socket import *
from threading import Thread, Lock
from time import sleep

from transportLayer.TCPLayer import TCPLayer
from transportLayer.TransportLayer import TransportLayer

class ServerTCP(TransportLayer):
  def __init__(self):
    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), 0))
    self.listenfdTCP.listen(1)
    self.lock = Lock()
    self.acceptConnectionsThread = Thread(target=acceptConnections,
                                          name='Accept Invitations',
                                          args=[self])
    self.acceptConnectionsThread.daemon = True
    self.tcpLayer: TCPLayer = None
    self.acceptConnectionsThread.start()

  def sendMessage(self, message):
    try:
      self.tcpLayer.sendMessage(message)
    except AttributeError:
      print("Você precisa ter uma conexão ativa para enviar uma mensagem")

  def recvMessage(self):
    if self.tcpLayer:
      try:
        return self.tcpLayer.recvMessage()
      except:
        return

  def closeSocket(self):
    self.listenfdTCP.close()

  def killConnection(self):
    try:
      self.tcpLayer.closeSocket()
      self.tcpLayer = None
      self.lock.release()
      print("Saí do release")
    except:
      print("Você precisa ter uma conexão ativa para fechar a conexão")
  
  def setTransportLayer(self, connectedSocket):
    self.lock.acquire()
    self.tcpLayer = TCPLayer(connectedSocket=connectedSocket)

  def updateTransportLayer(self, address, port):
    self.lock.acquire()
    self.tcpLayer = TCPLayer(address=address, port=port)

  def transportLayerExists(self)-> bool:
    self.lock.acquire()
    isThereTransportLayer = self.tcpLayer != None
    self.lock.release()
    return isThereTransportLayer

  def getPort(self):
    return self.listenfdTCP.getsockname()[1]


def acceptConnections(serverData: ServerTCP):
  while True:
    if not serverData.transportLayerExists():
      (connfd, address) = serverData.listenfdTCP.accept()
      serverData.setTransportLayer(connfd)