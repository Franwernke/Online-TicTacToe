#!/bin/python3

import os
import atexit
import signal
import sys
from TCPController import TCPController
from UDPController import UDPController
from repository import Repository
from server import Server
from log import Log

def main():
  atexit.register(cleanup)
  port = int(sys.argv[1])
  repository = Repository()
  log = Log()
  server = Server(repository)
  udpController = UDPController(port, server, log)
  udpController.acceptConnections()
  tcpController = TCPController(port, server, log)
  tcpController.acceptConnections()
  print("O servidor está escutando na porta", port)
  while True:
    continue

def cleanup():
  os.killpg(0, signal.SIGKILL)

if __name__ == "__main__":
  os.setpgrp()
  main()
