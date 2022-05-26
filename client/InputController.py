from Client import ClientDomain

class InputController:
  def __init__(self, client: ClientDomain) -> None:
    self.client = client

  def route(self, commandStr: str):
    command = commandStr.split()
    if command[0] == "new":
      if (len(command) < 3):
        print("Uso: new <username> <password>")
      else:
        self.client.createNewUser(command[1], command[2])

    elif command[0] == "pass":
      if (len(command) < 3):
        print("Uso: pass <old_password> <new_password>")
      else:
        self.client.changeUserPassword(command[1], command[2])

    elif command[0] == "in":
      if (len(command) < 3):
        print("Uso: in <username> <password>")
      else:
        self.client.loginUser(command[1], command[2], str(self.client.peerToPeerServer.getPort()))

    elif command[0] == "halloffame":
      self.client.showHallOfFame()

    elif command[0] == "l":
      self.client.showOnlinePlayers()

    elif command[0] == "call":
      if (len(command) < 2):
        print("Uso: call <opponent>")
      else:
        self.client.invitePlayer(command[1])

    elif command[0] == "play":
      if (len(command) < 3):
        print("Uso: play <linha> <coluna>")
      else:
        self.client.sendMove(command[1], command[2])

    elif command[0] == "delay":
      self.client.showLatency()

    elif command[0] == "over":
      self.client.endGame()

    elif command[0] == "out":
      self.client.logout()

    elif command[0] == "invite":
      self.client.receiveInvite(command[1])

    elif command[0] == "accept":
      self.client.acceptGame()

    elif command[0] == "refuse":
      self.client.refuseGame()

    else:
      print("Insira um comando válido!")