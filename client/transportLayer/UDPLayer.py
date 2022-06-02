#!/bin/python3
from socket import *

from transportLayer.TransportLayer import TransportLayer

ENCODING = 'utf-8'

class UDPLayer(TransportLayer):
  def __init__(self, address, port) -> None:
    self.sockfd = socket(AF_INET, SOCK_DGRAM)
    self.serverAddress = (address, int(port))

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)
    self.sockfd.sendto(message, self.serverAddress)

  def recvMessage(self):
    message = self.sockfd.recvfrom(4096)[0].decode(ENCODING)
    return message
