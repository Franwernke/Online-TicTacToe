#!/bin/python3

import os
import atexit
import signal
import sys
from TCPController import TCPController
from UDPController import UDPController
from repository import Repository
from server import Server

def main():
  atexit.register(cleanup)
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

def cleanup():
  os.killpg(0, signal.SIGKILL)

if __name__ == "__main__":
  os.setpgrp()
  main()
