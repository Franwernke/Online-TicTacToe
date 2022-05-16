from socket import *
import sys
import os
from Server import Server
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongPasswordException import WrongPasswordException

class TCPController:
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

    if command[0] == "new":
      self.server.createNewUser(command[1], command[2])

    # elif command[0] == "pass":
    #   if (len(command) < 3):
    #     print("Uso: pass <old_password> <new_password>")
    #   else:
    #     client.changeUserPassword(command[1], command[2])

    elif command[0] == "in":
      try:
        self.server.loginUser(command[1], command[2])
        self.sendMessage("OK", connfd)
      except UserNotFoundException as e:
        self.sendMessage(e.message, connfd)
      except WrongPasswordException as e:
        self.sendMessage(e.message, connfd)

    #   if user:
    #     if user.password == command[2]:
    #       response = "OK"
    #     else:
    #       response = "Senha incorreta"
    #   else:
    #     response = "Usuário não encontrado"

    #   if connfd == None:
    #     connfd.send(bytes(response, "utf-8"))
    #   else:
    #     connfd.sendto(bytes(response, "utf-8"), address)

    # elif command[0] == "halloffame":
    #   client.showHallOfFame()

    # elif command[0] == "l":
    #   client.showOnlinePlayers()

    # elif command[0] == "call":
    #   if (len(command) < 2):
    #     print("Uso: call <opponent>")
    #   else:
    #     client.invitePlayer(command[1])

    # elif command[0] == "play":
    #   if (len(command) < 3):
    #     print("Uso: play <linha> <coluna>")
    #   else:
    #     client.sendMove(command[1], command[2])

    # elif command[0] == "delay":
    #   client.showLatency()

    # elif command[0] == "over":
    #   client.endGame()

    # elif command[0] == "out":
    #   client.logout()