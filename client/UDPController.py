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

    fifoFd = open(self.fifoPath, "r")
    response = fifoFd.readline()
    fifoFd.close()

    return response

  def recvMessage(self):
    return self.sockfd.recvfrom(4096)[0].decode(ENCODING)

  def answerHeartbeat(self):
    message = bytes('heartbeat', ENCODING)
    self.sockfd.sendto(message, self.serverAddress)

'''
  client1 client2 servidor
  História:
    client1 -invite-> servidor
    servidor -invite-> client2 (servidor se comunica com FIFO do cliente no TCP e IP/Porta do cliente no UDP)
    client2 -accept-> servidor
    servidor -accept-> client1 (Servidor passa IPPorta do client2 para o client1)
'''