#!/bin/python3
from socket import *
from transportLayer.TransportLayer import TransportLayer

ENCODING = 'utf-8'

class TCPLayer(TransportLayer):
  def __init__(self, address=None, port=None, connectedSocket: socket=None) -> None:
    if not connectedSocket:
      self.sockfd = socket(AF_INET, SOCK_STREAM)
      self.serverAddress = (address, int(port))

      self.sockfd.connect(self.serverAddress)
    else:
      self.sockfd = connectedSocket

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)
    self.sockfd.send(message)

  def recvMessage(self):
    message = self.sockfd.recv(4096).decode(ENCODING)
    return message

  def restartConnection(self):
    try:
      self.sockfd.shutdown(SHUT_RDWR)
    except:
      pass
    self.sockfd = socket(AF_INET, SOCK_STREAM)
    self.sockfd.connect(self.serverAddress)
