#!/bin/python3
from socket import *

ENCODING = 'utf-8'

class TCPController:
  def __init__(self, address, port) -> None:

    self.sockfd = socket(AF_INET, SOCK_STREAM)
    self.serverAddress = (address, int(port))

    self.sockfd.connect(self.serverAddress)

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)

    self.sockfd.send(message)
    return self.sockfd.recv(4096).decode(ENCODING)

