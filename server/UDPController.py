import os
from socket import *
import sys
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
  
  def acceptConnections(self):
    childpid = os.fork()
    if childpid == 0:
      while True:
        recvline = self.listenfd.recvfrom(4096)
        if not recvline[1] in self.addresses:
          self.addresses.add(recvline[1])
          self.log.newConnection(recvline[1][0])
          self.sendHeartbeats(recvline[1])

        self.resolveMessage(recvline[0].decode("utf-8"), recvline[1])
        print("Received from UDP: " + recvline[0].decode("utf-8"))
        sys.stdout.flush()

  def sendMessage(self, messageStr, address):
    message = bytes(messageStr, "utf-8")
    self.listenfd.sendto(message, address)

  def resolveMessage(self, message, address):
    command = message.split()
    # self.writeInFifo()
    responseString = self.processCommand(command, address)

    if responseString != "DONOTANSWER":
      self.sendMessage(responseString, address)

  def sendHeartbeats(self, address):
    childPid = os.fork()
    
    if childPid == 0:
      while True:
        self.delayHeartbeat()
        self.sendMessage("heartbeat", address)
