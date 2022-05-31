import atexit
import os
import shutil
import signal
import sys
from input.InputController import InputController
from input.FeedbackController import FeedbackController
from input.Controller import Controller
from output.P2PRequester import P2PRequester
from output.Requester import Requester
from Router import Router
from transportLayer.serverTCP import ServerTCP
from transportLayer.TCPLayer import TCPLayer
from transportLayer.UDPLayer import UDPLayer
from Client import ClientDomain

BASEPATH = '/tmp/ep2/client/'

def main():
  atexit.register(cleanup)

  if os.path.exists(BASEPATH + str(os.getpid()) + '/FIFOs/'):
    shutil.rmtree(BASEPATH + str(os.getpid()) + '/FIFOs/')
  os.makedirs(BASEPATH + str(os.getpid()) + '/FIFOs/')

  serverResponseFifoPath = BASEPATH + str(os.getpid()) + '/FIFOs/serverResponseFifo'
  peerToPeerResponseFifoPath = BASEPATH + str(os.getpid()) + '/FIFOs/peerToPeerResponseFifo'
  latencyResponseFifoPath = BASEPATH + str(os.getpid()) + '/FIFOs/latencyResponseFifo'

  # 1
  if sys.argv[3] == "tcp":
    serverTransportLayer = TCPLayer(address=sys.argv[1], port=sys.argv[2])
  else:
    serverTransportLayer = UDPLayer(sys.argv[1], sys.argv[2])

  peerToPeerTransportLayer = ServerTCP()
  feedBackController = FeedbackController(serverResponseFifoPath, peerToPeerResponseFifoPath, latencyResponseFifoPath)

  # 2
  serverOutput = Requester(serverTransportLayer)
  peerToPeerOutput = P2PRequester(peerToPeerTransportLayer)

  # 3
  client = ClientDomain(serverOutput, peerToPeerOutput, feedBackController)
  
  # 4
  router = Router(client, feedBackController)

  # 5
  serverController = Controller(serverTransportLayer, router, 'Thread Controller do servidor')
  serverController.listen()

  peerToPeerController = Controller(peerToPeerTransportLayer, router, 'Thread Controller do PeerToPeer')
  peerToPeerController.listen()

  inputController = InputController(router)
  inputController.listenToKeyboard()
  sys.exit()

def cleanup():
  os.killpg(0, signal.SIGKILL)

if __name__ == "__main__":
  os.setpgrp()
  main()