#!/bin/python3

import sys
from TCPController import TCPController
from UDPController import UDPController
from Repository import Repository
from Server import Server

def main():
  port = int(sys.argv[1])
  repository = Repository()
  server = Server(repository)
  udpController = UDPController(port, server)
  udpController.acceptConnections()
  tcpController = TCPController(port, server)
  tcpController.acceptConnections()
  print("O servidor está escutando na porta", port)
  while True:
    continue

main()