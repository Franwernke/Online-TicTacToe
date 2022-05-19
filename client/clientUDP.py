#!/bin/python3
from socket import *
from client import Client

ENCODING = 'utf-8'

class ClientUDP(Client):
  def __init__(self, address, port) -> None:
    super().__init__()

    self.sockfd = socket(AF_INET, SOCK_DGRAM)
    self.serverAddress = (address, int(port))

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)

    self.sockfd.sendto(message, self.serverAddress)
    return self.sockfd.recvfrom(4096)[0].decode(ENCODING)

