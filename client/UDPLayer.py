#!/bin/python3
from socket import *

from TransportLayer import TransportLayer

ENCODING = 'utf-8'

class UDPLayer(TransportLayer):
  def __init__(self, address, port) -> None:
    self.sockfd = socket(AF_INET, SOCK_DGRAM)
    self.serverAddress = (address, int(port))

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)
    self.sockfd.sendto(message, self.serverAddress)

  def recvMessage(self):
    return self.sockfd.recvfrom(4096)[0].decode(ENCODING)

  def closeSocket(self):
    self.sockfd.close()
