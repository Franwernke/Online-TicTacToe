#!/bin/python3
from socket import *
from TransportLayer import TransportLayer

ENCODING = 'utf-8'

class TCPLayer(TransportLayer):
  def __init__(self, address, port) -> None:
    self.sockfd = socket(AF_INET, SOCK_STREAM)
    self.serverAddress = (address, int(port))

    self.sockfd.connect(self.serverAddress)

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)
    self.sockfd.send(message)

  def recvMessage(self):
    return self.sockfd.recv(4096).decode(ENCODING)

  def closeSocket(self):
    self.sockfd.close()
