from socket import *
import os
import sys

class ServerTCP:
  def __init__(self):
    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), 0))
    self.listenfdTCP.listen(1)

  def receiveInvitations(self):
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



'''
  Client TCP (2 sockets):
    Servidor - Cliente 
      socket TCP
      - enviar comandos
      - receber respostas do comando (FIFO)
      - heartbeat (FIFO)
      - invites de jogo (FIFO)
    Client - Client (serverTCP.py para quem recebe o invite, TCPController.py para quem envia invite)
      socket TCP
      - receber jogadas
      - receber comandos de partida (out)
  
  Client UDP (2 sockets):
    Servidor - Client
      socket UDP
      - enviar comandos
      - receber respostas do comando
      - heartbeat
      - invites de jogo
    Client - Client
      socket TCP
      - receber jogadas
      - receber comandos de partida (out)
'''