import os

class FifoRouter:
  def __init__(self, controller, commandResponseFifoPath):
    self.controller = controller
    self.commandResponseFifoPath = commandResponseFifoPath

    os.mkfifo(commandResponseFifoPath, 0o777)
  
  def listenServer(self):
    childPid = os.fork()
    if childPid == 0:
      while True:
        message = self.controller.recvMessage()
        command = message.split()[0]
        
        if command == 'heartbeat':
          self.controller.sendMessage(command)
        else:
          fifoFd = open(self.commandResponseFifoPath, "w")
          fifoFd.write(message)
          fifoFd.close()

  def readCommand(self):
    fifoFd = open(self.commandResponseFifoPath, "r")
    message = fifoFd.read()
    fifoFd.close()
    return message
