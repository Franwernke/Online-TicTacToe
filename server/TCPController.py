from socket import *
import sys
import os
from server import Server
from GenericController import GenericController

class TCPController(GenericController):
  def __init__(self, port: int, server: Server):
    self.server = server
    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), port))
    self.listenfdTCP.listen(1)

  def connect(self):
    self.listenfdTCP.connect()

  def acceptConnections(self):
    childpid = os.fork()
    if childpid == 0:
      while True:
        connfd: socket
        address: int
        (connfd, address) = self.listenfdTCP.accept()

        childpid = os.fork()
        if (childpid == 0):
          print("Um novo cliente se conectou!")
          self.listenfdTCP.close()
          self.address = address

          self.sendHeartbeats(connfd)

          recvline = connfd.recv(4096)
          while recvline:
            self.resolveMessage(recvline.decode("utf-8"), connfd)
            print("Received from TCP: " + recvline.decode("utf-8"))
            sys.stdout.flush()
            recvline = connfd.recv(4096)
          connfd.close()
          print("O cliente foi desconectado!")
          exit()
        else:
          connfd.close()
  
  def sendMessage(self, messageStr: str, connfd: socket):
    message = bytes(messageStr, "utf-8")
    connfd.send(message)

  def resolveMessage(self, message: str, connfd: socket):
    command = message.split()
    responseString = self.processCommand(command, self.address)

    if responseString != "DONOTANSWER":
      self.sendMessage(responseString, connfd)

  def sendHeartbeats(self, connfd):
    childPid = os.fork()
    
    if childPid == 0:
      while True:
        self.delayHeartbeat()
        self.sendMessage("heartbeat", connfd)
