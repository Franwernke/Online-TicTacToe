#!/bin/python3
from socket import *
from client import Client

ENCODING = 'utf-8'

class ClientTCP(Client):
  def __init__(self, address, port) -> None:
    super().__init__()

    self.sockfd = socket(AF_INET, SOCK_STREAM)
    self.serverAddress = (address, int(port))

    self.sockfd.connect(self.serverAddress)

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)

    self.sockfd.send(message)
    return self.sockfd.recv(4096).decode(ENCODING)

