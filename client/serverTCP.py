from socket import *
import os
import sys

class ServerTCP:
  def __init__(self):
    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), 0))
    self.listenfdTCP.listen(1)

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

  def getPort(self):
    return self.listenfdTCP.getsockname()[1]
