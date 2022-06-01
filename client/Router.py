from multiprocessing.dummy import Array
from Client import ClientDomain
from input.FeedbackController import FifoChoice
from input.FeedbackController import FeedbackController

class Router:
  def __init__(self, client: ClientDomain, feedBackController: FeedbackController):
    self.client = client
    self.feedBackController = feedBackController

  def routeReponse(self, response: list):
    responseStr = ' '.join(response)
    if response[0] == "play":
      self.client.receivePlay()
    elif response[0] == "over":
      self.client.endGame()
    elif response[0] == "latency":
      self.feedBackController.sendResponse(responseStr, FifoChoice.latency)
    elif response[0] == "invite":
      self.feedBackController.sendResponse(responseStr, FifoChoice.peerToPeerResponse)
    elif response[0] == "accept":
      self.feedBackController.sendResponse(responseStr, FifoChoice.peerToPeerResponse)
    elif response[0] == "refuse":
      self.feedBackController.sendResponse(responseStr, FifoChoice.peerToPeerResponse)
    else:
      self.feedBackController.sendResponse(responseStr, FifoChoice.serverResponse)

  def routeRequest(self, request: list):
    if request[0] == "new":
      self.client.createNewUser(request[1], request[2])

    elif request[0] == "pass":
      self.client.changeUserPassword(request[1], request[2])

    elif request[0] == "in":
      self.client.loginUser(request[1], request[2], str(self.client.peerToPeerOutput.getPort()))

    elif request[0] == "halloffame":
      self.client.showHallOfFame()

    elif request[0] == "l":
      self.client.showOnlinePlayers()

    elif request[0] == "call":
      self.client.invitePlayer(request[1])

    elif request[0] == "play":
      self.client.sendMove(int(request[1]), int(request[2]))

    elif request[0] == "delay":
      self.client.showLatency()

    elif request[0] == "over":
      self.client.endGame()

    elif request[0] == "out":
      self.client.logout()

    elif request[0] == "invite":
      self.client.receiveInvite(request[1])

    elif request[0] == "accept":
      self.client.acceptGame()

    elif request[0] == "refuse":
      self.client.refuseGame()

    elif request[0] == "heartbeat":
      self.client.sendHeartbeat()

    elif request[0] == "finish":
      self.client.receiveEndgame()
  
    elif request[0] == "bye":
      self.client.disconnect()

  def route(self, messageStr: str):
    message = messageStr.split()
    if message[0] == "P":
      self.routeReponse(message[1:])
    else:
      self.routeRequest(message)
