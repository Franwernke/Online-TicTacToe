from transportLayer.TransportLayer import TransportLayer
from Router import Router
from threading import Thread

class Controller:
  def __init__(self, transportLayer: TransportLayer, router: Router, threadName: str):
    self.transportLayer = transportLayer
    self.router = router
    self.threadName = threadName
    self.listenThread = Thread(target=listenThread, args=[self], name=threadName)
    self.listenThread.daemon = True

  def listen(self):
    self.listenThread.start()

def listenThread(controller: Controller):
  while True:

    try:
      message = controller.transportLayer.recvMessage()
    except:
      message = ""

    if message:
      controller.router.route(message)
