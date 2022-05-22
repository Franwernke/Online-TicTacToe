import os

class FifoRouter:
  def __init__(self, controller, commandResponseFifoPath, inviteFifoPath):
    self.controller = controller
    self.commandResponseFifoPath = commandResponseFifoPath
    self.inviteFifoPath = inviteFifoPath

    os.mkfifo(commandResponseFifoPath, 0o777)
    os.mkfifo(inviteFifoPath, 0o777)
  
  def listenServer(self):
    childPid = os.fork()
    if childPid == 0:
      while True:
        message = self.controller.recvMessage()
        command = message.split()[0]
        
        if command == 'heartbeat':
          self.controller.answerHeartbeat()
        else:
          if command == 'invite':
            fifoFd = open(self.inviteFifoPath, "w")
          else:
            fifoFd = open(self.commandResponseFifoPath, "w")
        
          fifoFd.write(message)
          fifoFd.close()




