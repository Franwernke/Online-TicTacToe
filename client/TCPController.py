#!/bin/python3
from socket import *

ENCODING = 'utf-8'

class TCPController:
  def __init__(self, address, port, commandReponseFifoPath) -> None:

    self.sockfd = socket(AF_INET, SOCK_STREAM)
    self.serverAddress = (address, int(port))

    self.sockfd.connect(self.serverAddress)

    self.fifoPath = commandReponseFifoPath

  def sendMessage(self, messageStr):
    message = bytes(messageStr, ENCODING)

    self.sockfd.send(message)

    fifoFd = open(self.fifoPath, "r")
    response = fifoFd.readline()
    fifoFd.close()

    return response

  def recvMessage(self):
    return self.sockfd.recv(4096).decode(ENCODING)
  
  def answerHeartbeat(self):
    message = bytes('heartbeat', ENCODING)
    self.sockfd.send(message)
