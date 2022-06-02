#!/bin/python3

import sys
from time import sleep
from TCPController import TCPController
from UDPController import UDPController
from repository import Repository
from server import Server
from log import Log

def main():
  port = int(sys.argv[1])
  repository = Repository()
  log = Log()
  server = Server(repository, log)
  udpController = UDPController(port, server, log)
  udpController.acceptConnections()
  tcpController = TCPController(port, server, log)
  tcpController.acceptConnections()
  print("O servidor está escutando na porta", port)
  while True:
    sleep(100)

if __name__ == "__main__":
  main()
