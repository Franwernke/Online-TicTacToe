#!/bin/python3
from socket import *

ENCODING = 'utf-8'

class UDPController:
  def __init__(self, address, port) -> None:

    self.sockfd = socket(AF_INET, SOCK_DGRAM)
    self.serverAddress = (address, int(port))

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)

    self.sockfd.sendto(message, self.serverAddress)
    return self.sockfd.recvfrom(4096)[0].decode(ENCODING)
