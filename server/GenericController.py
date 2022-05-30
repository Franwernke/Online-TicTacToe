from time import sleep
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongPasswordException import WrongPasswordException
from exceptions.UserAlreadyExists import UserAlreadyExists
from exceptions.UserAlreadyLoggedIn import UserAlreadyLoggedIn
from exceptions.UserIsAlreadyInGame import UserIsAlreadyInGame
from exceptions.UserIsNotAvailable import UserIsNotAvailable

class GenericController:
  def delayHeartbeat(self):
    sleep(10)

  def processCommand(self, command, address):
    if command[0] == "new":
      try:
        self.server.createNewUser(command[1], command[2])
        return "OK"
      except UserAlreadyExists as e:
        return e.message

    elif command[0] == "pass":
      try:
        self.server.changePassword(command[1], command[2], command[3])
        return "OK"
      except UserNotFoundException as e:
        return e.message
      except WrongPasswordException as e:
        return e.message

    elif command[0] == "in":
      try:
        self.server.loginUser(command[1], command[2], (address[0], command[3]))
        return "OK"
      except UserNotFoundException as e:
        return e.message
      except WrongPasswordException as e:
        return e.message
      except UserAlreadyLoggedIn as e:
        return e.message
      except Exception as e:
        print(e)

    elif command[0] == "halloffame":
      return str(self.server.showHallOfFame())

    elif command[0] == "l":
      return str(self.server.showOnlinePlayers())

    elif command[0] == "call":
      try:
        userSession = self.server.invitePlayer(command[1], command[2])
        return "OK " + userSession.ip + " " + userSession.port 
      except UserIsAlreadyInGame as e:
        return e.message
      except UserIsNotAvailable as e:
        return e.message

    elif command[0] == "out":
      self.server.logout(command[1])
      return "OK"
    
    elif command[0] == "startgame":
      self.server.startgame(command[1], command[2])
      return "OK"

    elif command[0] == "won":
      self.server.setWinner(command[1], command[2])
      return "OK"

    elif command[0] == "draw":
      self.server.drawGame(command[1], command[2])
      return "OK"

    elif command[0] == "over":
      self.server.endgame(command[1], command[2])
      return "OK"

    elif command[0] == "heartbeat":
      self.server.handleHeartbeat(address)
      return "DONOTANSWER"