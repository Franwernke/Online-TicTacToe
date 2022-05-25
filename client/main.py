import atexit
import os
import shutil
import signal
import sys
from FifoRouter import FifoRouter
from serverTCP import ServerTCP
from TCPController import TCPController
from UDPController import UDPController
from client import Client

BASEPATH = '/tmp/ep2/client/'

def main():
  if os.path.exists(BASEPATH + str(os.getpid()) + '/FIFOs/'):
    shutil.rmtree(BASEPATH + str(os.getpid()) + '/FIFOs/')
  os.makedirs(BASEPATH + str(os.getpid()) + '/FIFOs/')

  commandResponseFifoPath = BASEPATH + str(os.getpid()) + '/FIFOs/command'

  if sys.argv[3] == "tcp":
    serverController = TCPController(sys.argv[1], sys.argv[2])
  else:
    serverController = UDPController(sys.argv[1], sys.argv[2])

  serverPeerToPeer = ServerTCP()

  fifoRouter = FifoRouter(serverController, commandResponseFifoPath)
  fifoRouter.listenServer()

  client = Client(serverController, serverPeerToPeer, fifoRouter)

  atexit.register(cleanup)

  command = input("JogoDaVelha> ").split()  
  while command[0] != "bye":
    if command[0] == "new":
      if (len(command) < 3):
        print("Uso: new <username> <password>")
      else:
        client.createNewUser(command[1], command[2])

    elif command[0] == "pass":
      if (len(command) < 3):
        print("Uso: pass <old_password> <new_password>")
      else:
        client.changeUserPassword(command[1], command[2])

    elif command[0] == "in":
      if (len(command) < 3):
        print("Uso: in <username> <password>")
      else:
        client.loginUser(command[1], command[2], str(serverPeerToPeer.getPort()))

    elif command[0] == "halloffame":
      client.showHallOfFame()

    elif command[0] == "l":
      client.showOnlinePlayers()

    elif command[0] == "call":
      if (len(command) < 2):
        print("Uso: call <opponent>")
      else:
        client.invitePlayer(command[1])

    elif command[0] == "play":
      if (len(command) < 3):
        print("Uso: play <linha> <coluna>")
      else:
        client.sendMove(command[1], command[2])

    elif command[0] == "delay":
      client.showLatency()

    elif command[0] == "over":
      client.endGame()

    elif command[0] == "out":
      client.logout()
    elif command[0] == "accept":
      client.acceptGame(command[1])
    elif command[0] == "refuse":
      client.refuseGame(command[1])
    else:
      print("Insira um comando válido!")

    command = input("JogoDaVelha> ").split()
  sys.exit()

def cleanup():
  os.killpg(-1, signal.SIGKILL)

if __name__ == "__main__":
  os.setpgrp()
  main()