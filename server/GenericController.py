from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongPasswordException import WrongPasswordException
from exceptions.UserAlreadyExists import UserAlreadyExists

class GenericController:
  def getResponse(self, command):

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
        self.server.loginUser(command[1], command[2])
        return "OK"
      except UserNotFoundException as e:
        return e.message
      except WrongPasswordException as e:
        return e.message

    elif command[0] == "halloffame":
       return str(self.server.showHallOfFame())

    # elif command[0] == "l":
    #   client.showOnlinePlayers()

    # elif command[0] == "call":
    #   if (len(command) < 2):
    #     print("Uso: call <opponent>")
    #   else:
    #     client.invitePlayer(command[1])

    # elif command[0] == "play":
    #   if (len(command) < 3):
    #     print("Uso: play <linha> <coluna>")
    #   else:
    #     client.sendMove(command[1], command[2])

    # elif command[0] == "delay":
    #   client.showLatency()

    # elif command[0] == "over":
    #   client.endGame()

    # elif command[0] == "out":
    #   client.logout()