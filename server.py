#!/bin/python3

from asyncore import read
import os
from socket import *
import string
import sys

class Server:
  def __init__(self, port):
    self.listenfd = socket(AF_INET, SOCK_STREAM)
    self.listenfd.bind((gethostname(), port))
    print(gethostname())
    self.listenfd.listen(1)

  def connect(self):
    self.listenfd.connect()

  def acceptConnections(self):
    while True:
      connfd: socket
      address: int
      (connfd, address) = self.listenfd.accept()

      childpid = os.fork()
      if (childpid == 0):
        self.listenfd.close()

        while recvline:
          recvline = connfd.recv(4096)
          print("Received " + str(recvline))
        connfd.close()
      else:
        connfd.close()

def main():
  server = Server(int(sys.argv[1]))
  server.acceptConnections()

main()