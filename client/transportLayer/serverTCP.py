from socket import *
from threading import Thread, Lock

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
      return self.tcpLayer.recvMessage()

  def closeSocket(self):
    self.listenfdTCP.close()

  def killConnection(self):
    try:
      print("kill connection")
      self.tcpLayer.closeSocket()
      self.tcpLayer = None
      self.lock.release()
      print("Release killconnection")
    except AttributeError:
      print("Você precisa ter uma conexão ativa para fechar a conexão")
  
  def setTransportLayer(self, connectedSocket):
    self.lock.acquire()
    self.tcpLayer = TCPLayer(connectedSocket=connectedSocket)

  def transportLayerExists(self)-> bool:
    print("Antes do acquire")
    self.lock.acquire()
    print("Depois do acquire")
    isThereTransportLayer = self.tcpLayer != None
    self.lock.release()
    print("Release transportLayer")
    return isThereTransportLayer

  def updateTransportLayer(self, address, port):
    self.tcpLayer = TCPLayer(address=address, port=port)

  def getPort(self):
    return self.listenfdTCP.getsockname()[1]


def acceptConnections(serverData: ServerTCP):
  while True:
    if not serverData.transportLayerExists():
      (connfd, address) = serverData.listenfdTCP.accept()
      serverData.setTransportLayer(connfd)