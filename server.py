#!/bin/python3

import os
from socket import *
import sys

class User:
  def __init__(self, username, password) -> None:
    self.username = username
    self.password = password

class Repository:
  def __init__(self):
    if not os.path.exists("/tmp/ep2/users"):
      os.makedirs("/tmp/ep2/users")

  def createNewUser(self, user, password):
    file = open("/tmp/ep2/users/" + user, "w")
    file.write(password)

  def getUser(self, user):
    if os.path.exists("/tmp/ep2/users" + user):
      file = open("/tmp/ep2/users/" + user, "r")
      password = file.read()
      username = user
      return User(username, password)
    else:
      return None


class Server:
  def __init__(self, port):
    self.listenfdTCP = socket(AF_INET, SOCK_STREAM)
    self.listenfdTCP.bind((str(INADDR_ANY), port))
    self.listenfdTCP.listen(1)

    self.listenfdUDP = socket(AF_INET, SOCK_DGRAM)
    self.listenfdUDP.bind((str(INADDR_ANY), port))

    self.repository = Repository()

    print("O servidor está escutando na porta", port)

  def connect(self):
    self.listenfdTCP.connect()

  def acceptTCPConnections(self):
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
          self.parseMessage(recvline.decode("utf-8"), address, connfd)
          print("Received from TCP: " + recvline.decode("utf-8"))
          sys.stdout.flush()
          recvline = connfd.recv(4096)
        connfd.close()
        print("O cliente foi desconectado!")
        exit()
      else:
        connfd.close()

  def acceptUDPConnections(self):

    while True:
      recvline = self.listenfdUDP.recvfrom(4096)
      self.parseMessage(recvline[0].decode("utf-8"), recvline[1])
      print("Received from UDP: " + recvline[0].decode("utf-8"))
      sys.stdout.flush()

  def parseMessage(self, message, address, connfd = None):
    command = message.split()

    if command[0] == "new":
      self.repository.createNewUser(command[1], command[2])

    # elif command[0] == "pass":
    #   if (len(command) < 3):
    #     print("Uso: pass <old_password> <new_password>")
    #   else:
    #     client.changeUserPassword(command[1], command[2])

    elif command[0] == "in":
      user = self.repository.getUser(command[1])

      if user:
        if user.password == command[2]:
          response = "OK"
        else:
          response = "Senha incorreta"
      else:
        response = "Usuário não encontrado"

      if connfd == None:
        connfd.send(bytes(response, "utf-8"))
      else:
        connfd.sendto(bytes(response, "utf-8"), address)

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



def main():
  server = Server(int(sys.argv[1]))

  childpid = os.fork()
  if (childpid == 0):
    server.acceptTCPConnections()
  else:
    server.acceptUDPConnections()

main()