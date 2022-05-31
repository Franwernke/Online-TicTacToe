from socket import *
from threading import Thread, Lock

from transportLayer.TCPLayer import TCPLayer
from transportLayer.TransportLayer import TransportLayer

class ServerTCP(TransportLayer):
  def __init__(self):
    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), 0))
    self.listenfdTCP.listen(1)
    self.acceptConnectionsThread = Thread(target=acceptConnections,
                                          name='Accept Invitations',
                                          args=[self])
    self.acceptConnectionsThread.start()
    self.tcpLayer: TCPLayer = None

  def sendMessage(self, message):
    try:
      self.tcpLayer.sendMessage(message)
    except AttributeError:
      print("Você precisa ter uma conexão ativa para enviar uma mensagem")

  def recvMessage(self):
    if self.tcpLayer:
      return self.tcpLayer.recvMessage()

  def closeSocket(self):
    self.listenfdTCP.close()

  def killConnection(self):
    try:
      self.tcpLayer.closeSocket()
      self.tcpLayer = None
      self.lock.acquire()
    except AttributeError:
      print("Você precisa ter uma conexão ativa para fechar a conexão")
  
  def setTransportLayer(self, connectedSocket):
    self.tcpLayer = TCPLayer(connectedSocket=connectedSocket)

  def updateTransportLayer(self, address, port):
    self.tcpLayer = TCPLayer(address=address, port=port)

  def getPort(self):
    return self.listenfdTCP.getsockname()[1]


def acceptConnections(serverData: ServerTCP):
  while True:
    (connfd, address) = serverData.listenfdTCP.accept()
    if not serverData.tcpLayer:
      serverData.setTransportLayer(connfd)