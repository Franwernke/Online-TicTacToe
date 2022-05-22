#!/bin/python3
from socket import *

ENCODING = 'utf-8'

class UDPController:
  def __init__(self, address, port, commandReponseFifoPath) -> None:

    self.sockfd = socket(AF_INET, SOCK_DGRAM)
    self.serverAddress = (address, int(port))

    self.fifoPath = commandReponseFifoPath

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)

    self.sockfd.sendto(message, self.serverAddress)

    fifoFd = open(self.fifoPath, "r")
    response = fifoFd.readline()
    fifoFd.close()

    return response

  def recvMessage(self):
    return self.sockfd.recvfrom(4096)[0].decode(ENCODING)

  def answerHeartbeat(self):
    message = bytes('heartbeat', ENCODING)
    self.sockfd.sendto(message, self.serverAddress)

