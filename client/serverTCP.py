from socket import *
import os
import sys

BASEPATH = '/tmp/ep2/client/'

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
          self.listenfdTCP.close()
          self.address = address

          recvline = connfd.recv(4096)
          invitationsPath = BASEPATH + 'FIFOs/invitations/'
          os.makedirs(invitationsPath)
          user = recvline.decode("utf-8").split()[1]
          os.mkfifo(invitationsPath + user, 0o777)
  
          print("Novo convite:" + user)
          sys.stdout.flush()

          invitationFifo = open(invitationsPath + user, "r")
          connfd.send(bytes(invitationFifo.read(), 'utf-8'))
          invitationFifo.close()


          recvline = connfd.recv(4096)
          while recvline:
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