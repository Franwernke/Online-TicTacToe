from socket import *

class TransportLayer:
  
  def sendMessage(self, messageStr) -> None:
    pass

  def recvMessage(self) -> str:
    pass

  def closeSocket(self):
    self.sockfd.shutdown(SHUT_RDWR)
    self.sockfd.close()