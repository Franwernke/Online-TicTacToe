import os
from socket import *
import sys
from server import Server

class UDPController:
  def __init__(self, port, server: Server):
    self.server = server
    self.listenfd = socket(AF_INET, SOCK_DGRAM)
    self.listenfd.bind((str(INADDR_ANY), port))
  
  def acceptConnections(self):
    childpid = os.fork()
    if childpid == 0:
      while True:
        recvline = self.listenfd.recvfrom(4096)
        self.resolveMessage(recvline[0].decode("utf-8"), recvline[1])
        print("Received from UDP: " + recvline[0].decode("utf-8"))
        sys.stdout.flush()

  def resolveMessage(self, message, address):
    command = message.split()

    if command[0] == "new":
      self.server.createNewUser(command[1], command[2])
        
    # elif command[0] == "pass":
    #   if (len(command) < 3):
    #     print("Uso: pass <old_password> <new_password>")
    #   else:
    #     client.changeUserPassword(command[1], command[2])

    # elif command[0] == "in":
    #   user = self.repository.getUser(command[1])

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