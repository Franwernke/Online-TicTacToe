from os import mkfifo

class FifoChoice():
  latency = "LATENCY"
  serverResponse = "SERVERRESPONSE"
  peerToPeerResponse = "P2PRESPONSE"

class FeedbackController():
  def __init__(self, serverResponseFifoPath: str, peerToPeerResponseFifoPath: str, latencyResponseFifoPath: str) -> None:
    self.serverResponseFifoPath = serverResponseFifoPath
    self.peerToPeerResponseFifoPath = peerToPeerResponseFifoPath
    self.latencyResponseFifoPath = latencyResponseFifoPath

    mkfifo(serverResponseFifoPath, 0o777)
    mkfifo(peerToPeerResponseFifoPath, 0o777)
    mkfifo(latencyResponseFifoPath, 0o777)

  def openIntendedFifo(self, intendedFifo: str, mode: str):
    if intendedFifo == FifoChoice.serverResponse:
      return open(self.serverResponseFifoPath, mode)
    elif intendedFifo == FifoChoice.latency:
      return open(self.latencyResponseFifoPath, mode)
    elif intendedFifo == FifoChoice.peerToPeerResponse:
      return open(self.peerToPeerResponseFifoPath, mode)
  
  def sendResponse(self, response: str, intendedFifo: str) -> None:
    fifo = self.openIntendedFifo(intendedFifo, "w")
    fifo.write(response)

  def recvResponse(self, intendedFifo: str) -> str:
    fifo = self.openIntendedFifo(intendedFifo, "r")
    return fifo.read()