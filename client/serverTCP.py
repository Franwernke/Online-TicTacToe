from socket import *
from threading import Thread
from Response import Response

ENCODING = 'utf-8'

class ServerTCP:
  def __init__(self, commandHandler):
    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), 0))
    self.listenfdTCP.listen(1)
    self.commandHandler = commandHandler
    self.keepConnectionAlive = True
    self.acceptConnectionsThread = Thread(target=acceptConnections,
                                          name='Accept Invitations',
                                          args=[self])
    self.acceptConnectionsThread.start()

  def sendMessage(self, message):
    message = bytes(message, ENCODING)
    try:
      self.connfd.send(message)
    except AttributeError:
      print("Você precisa ter uma conexão ativa para enviar uma mensagem")

  def getPort(self):
    return self.listenfdTCP.getsockname()[1]

  def killConnection(self):
    self.keepConnectionAlive = False

def acceptConnections(serverData: ServerTCP):
  while True:
    (connfd, address) = serverData.listenfdTCP.accept()
    serverData.connfd = connfd
    recvline = connfd.recv(4096)
    while recvline and serverData.keepConnectionAlive:
      print("Recebi:", recvline.decode(ENCODING))
      serverData.commandHandler.handle(recvline.decode(ENCODING))
      recvline = connfd.recv(4096)

    connfd.close()
    serverData.keepConnectionAlive = True
  