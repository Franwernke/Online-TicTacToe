import atexit
import os
import shutil
import signal
import sys
from FifoRouter import FifoRouter
from InputController import InputController
from OpponentCommands import OpponentCommands
from serverTCP import ServerTCP
from TCPLayer import TCPLayer
from UDPLayer import UDPLayer
from TransportLayer import TransportLayer
from client import ClientDomain

BASEPATH = '/tmp/ep2/client/'

def main():
  atexit.register(cleanup)

  if os.path.exists(BASEPATH + str(os.getpid()) + '/FIFOs/'):
    shutil.rmtree(BASEPATH + str(os.getpid()) + '/FIFOs/')
  os.makedirs(BASEPATH + str(os.getpid()) + '/FIFOs/')

  commandResponseFifoPath = BASEPATH + str(os.getpid()) + '/FIFOs/command'

  if sys.argv[3] == "tcp":
    serverController = TCPLayer(sys.argv[1], sys.argv[2])
  else:
    serverController = UDPLayer(sys.argv[1], sys.argv[2])

  fifoRouter = FifoRouter(serverController, commandResponseFifoPath)
  fifoRouter.listenServer()

  client = ClientDomain(fifoRouter)

  commandHandler = OpponentCommands(client)

  peerToPeerServer = ServerTCP(commandHandler)

  client.peerToPeerServer = peerToPeerServer

  client.serverController = serverController

  router = InputController(client)

  command = input("JogoDaVelha> ")
  while command != 'bye':
    router.route(command)
    command = input("JogoDaVelha> ")

  sys.exit()

def cleanup():
  os.killpg(0, signal.SIGKILL)

if __name__ == "__main__":
  os.setpgrp()
  main()