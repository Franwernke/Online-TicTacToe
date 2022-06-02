from socket import *
import sys
from threading import Thread
from server import Server
from GenericController import GenericController
from log import Log

class TCPController(GenericController):
  def __init__(self, port: int, server: Server, log: Log):
    self.server = server
    self.log = log

    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), port))
    self.listenfdTCP.listen(1)
    self.acceptConnectionsThread = Thread(target=acceptConnectionsThreadFunc, name='Accept connections', args=[self])

  def acceptConnections(self):
    self.acceptConnectionsThread.start()
  
  def sendMessage(self, messageStr: str, connfd: socket):
    message = bytes(messageStr, "utf-8")
    connfd.send(message)

  def resolveMessage(self, message: str, connfd: socket, address):
    command = message.split()
    responseString = self.processCommand(command, address)

    if responseString != "DONOTANSWER":
      self.sendMessage(responseString, connfd)

def acceptConnectionsThreadFunc(controller: TCPController):
  while True:
    connfd: socket
    (connfd, address) = controller.listenfdTCP.accept()

    threadHandleConnection = Thread(target=handleConnection, name='Address ' + str(address) + ' thread', args=[controller, connfd, address])
    threadHandleConnection.start()

def handleConnection(controller: TCPController, connfd: socket, address):
  controller.log.newConnection(address[0])
  print("Um novo cliente se conectou!")

  threadHeartbeats = Thread(target=sendHeartbeats, name='Heartbeat of ' + str(address), args=[controller, connfd])
  threadHeartbeats.start()

  recvline = connfd.recv(4096)
  while recvline:
    controller.resolveMessage(recvline.decode("utf-8"), connfd, address)
    print("Received from TCP: " + recvline.decode("utf-8"))
    sys.stdout.flush()
    recvline = connfd.recv(4096)
  connfd.close()
  print("O cliente foi desconectado!")

def sendHeartbeats(controller: TCPController, connfd: socket):
  while True:
    controller.delayHeartbeat()
    controller.sendMessage("heartbeat", connfd)
