from transportLayer.TransportLayer import TransportLayer

class Requester:
  def __init__(self, transportLayer: TransportLayer):
    self.transportLayer = transportLayer
  
  def sendMessage(self, message: str):
    self.transportLayer.sendMessage(message)
