from time import sleep
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.WrongPasswordException import WrongPasswordException
from exceptions.UserAlreadyExists import UserAlreadyExists
from exceptions.UserAlreadyLoggedIn import UserAlreadyLoggedIn

class GenericController:
  def delayHeartbeat(self):
    sleep(1)


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
      self.server.invitePlayer(command[1], command[2])

    # elif command[0] == "play":
    #   if (len(command) < 3):
    #     print("Uso: play <linha> <coluna>")
    #   else:
    #     client.sendMove(command[1], command[2])

    # elif command[0] == "delay":
    #   client.showLatency()

    # elif command[0] == "over":
    #   client.endGame()

    elif command[0] == "out":
      self.server.logout(command[1])
      return "OK"

    elif command[0] == "heartbeat":
      self.server.handleHeartbeat(address)
      return "DONOTANSWER"