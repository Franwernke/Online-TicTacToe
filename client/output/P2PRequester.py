from transportLayer.serverTCP import ServerTCP
from output.Requester import Requester

class P2PRequester(Requester):
  def __init__(self, transportLayer: ServerTCP) -> None:
    super().__init__(transportLayer)
    self.transportLayer: ServerTCP

  def killConnection(self):
    self.transportLayer.killConnection()

  def updateTransportLayer(self, address, port):
    self.transportLayer.updateTransportLayer(address, port)
  
  def getPort(self):
    return self.transportLayer.getPort()