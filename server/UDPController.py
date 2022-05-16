import os
from socket import *
import sys
from server import Server
from GenericController import GenericController

class UDPController(GenericController):
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

  def sendMessage(self, messageStr, address):
    message = bytes(messageStr, "utf-8")
    self.listenfd.sendto(message, address)

  def resolveMessage(self, message, address):
    command = message.split()
    responseString = self.getResponse(command)
    self.sendMessage(responseString, address)
