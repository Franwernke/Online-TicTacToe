from socket import *
import sys
from threading import Thread, Lock
from server import Server
from GenericController import GenericController
from log import Log

class TCPSocketWrapper:
  def __init__(self, connfd: socket, address: tuple) -> None:
    self.connfd = connfd
    self.address = address
    self.keepHeartbeating = True
    self.lock = Lock()

class TCPController(GenericController):
  def __init__(self, port: int, server: Server, log: Log):
    self.server = server
    self.log = log

    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), port))
    self.listenfdTCP.listen(1)
    self.acceptConnectionsThread = Thread(target=acceptConnectionsThreadFunc, name='Accept connections', args=[self])
    self.acceptConnectionsThread.daemon = True

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
    threadHandleConnection.daemon = True
    threadHandleConnection.start()

def handleConnection(controller: TCPController, connfd: socket, address):
  disconnected = False
  controller.log.newConnection(address[0])
  print("Um novo cliente se conectou!")

  socketWrapperForHeartbeats = TCPSocketWrapper(connfd, address)

  threadHeartbeats = Thread(target=sendHeartbeats, name='Heartbeat of ' + 
                            str(address), args=[controller, socketWrapperForHeartbeats])
  threadHeartbeats.daemon = True
  threadHeartbeats.start()

  recvline = connfd.recv(4096)
  while recvline:
    if recvline.decode("utf-8") == "bye":
      disconnected = True

    if recvline.decode("utf-8") != "heartbeat":
      controller.resolveMessage(recvline.decode("utf-8"), connfd, address)

    print("Received from TCP: " + recvline.decode("utf-8"))
    sys.stdout.flush()
    recvline = connfd.recv(4096)

  socketWrapperForHeartbeats.lock.acquire()

  socketWrapperForHeartbeats.keepHeartbeating = False
  connfd.shutdown(SHUT_RDWR)
  connfd.close()

  socketWrapperForHeartbeats.lock.release()
  
  if disconnected:
    print("O cliente foi desconectado!")
  else:
    print("Desconexão inesperada do cliente!")
    controller.log.unexpectedDisconnect(address[0])



def sendHeartbeats(controller: TCPController, socketWrapper: TCPSocketWrapper):
  while socketWrapper.keepHeartbeating:
    controller.delayHeartbeat()
    socketWrapper.lock.acquire()
    if socketWrapper.keepHeartbeating:
      controller.sendMessage("heartbeat", socketWrapper.connfd)
    socketWrapper.lock.release()

  controller.server.disconnectDueToTimeout(socketWrapper.address)

