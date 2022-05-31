from transportLayer.TransportLayer import TransportLayer
from Router import Router
from threading import Thread

class Controller:
  def __init__(self, transportLayer: TransportLayer, router: Router, threadName: str):
    self.transportLayer = transportLayer
    self.router = router
    self.threadName = threadName
    self.listenThread = Thread(target=listenThread, args=[self], name=threadName)

  def listen(self):
    self.listenThread.start()

def listenThread(controller: Controller):
  while True:
    message = controller.transportLayer.recvMessage()
    if message:
      controller.router.route(message)
