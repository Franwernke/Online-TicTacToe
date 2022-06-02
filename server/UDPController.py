from socket import *
import sys
from threading import Thread
from server import Server
from GenericController import GenericController
from log import Log

class UDPController(GenericController):
  def __init__(self, port, server: Server, log: Log):
    self.server = server
    self.log = log

    self.listenfd = socket(AF_INET, SOCK_DGRAM)
    self.listenfd.bind((str(INADDR_ANY), port))
    self.addresses = set()
    self.acceptConnectionsThread = Thread(target=acceptConnectionsThreadFunc, name='Accept connections thread', args=[self])

  def acceptConnections(self):
    self.acceptConnectionsThread.start()

  def sendMessage(self, messageStr: str, address):
    message = bytes(messageStr, "utf-8")
    self.listenfd.sendto(message, address)

  def resolveMessage(self, message: str, address):
    command = message.split()
    # self.writeInFifo()
    responseString = self.processCommand(command, address)

    if responseString != "DONOTANSWER":
      self.sendMessage(responseString, address)

def acceptConnectionsThreadFunc(controller: UDPController):
  while True:
    recvline = controller.listenfd.recvfrom(4096)

    if not recvline[1] in controller.addresses:
      controller.addresses.add(recvline[1])
      controller.log.newConnection(recvline[1][0])

      sendHeartbeatsThread = Thread(target=sendHeartbeats, name='Address ' + str(recvline[1]) + ' heartbeat', args=[controller, recvline[1]])
      sendHeartbeatsThread.start()

    controller.resolveMessage(recvline[0].decode("utf-8"), recvline[1])
    print("Received from UDP: " + recvline[0].decode("utf-8"))
    sys.stdout.flush()

def sendHeartbeats(controller: UDPController, address):
  while True:
    controller.delayHeartbeat()
    controller.sendMessage("heartbeat", address)
