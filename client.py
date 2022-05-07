#!/bin/python3

from clientStates import *

class Client:
  def __init__(self) -> None:
    self.state = InitialState()
    pass

  def changeState(self, newState):
    self.state = newState

  def createNewUser(self, user, password):
    self.state.createNewUser(self, user, password)

  def changeUserPassword(self, oldPassword, newPassword):
    self.state.changeUserPassword(self, oldPassword, newPassword)
  
  def loginUser(self, user, password):
    self.state.loginUser(self, user, password)
  
  def showHallOfFame(self):
    self.state.showHallOfFame(self)
  
  def showOnlinePlayers(self):
    self.state.showOnlinePlayers(self)

  def invitePlayer(self, opponent):
    self.state.invitePlayer(self, opponent)

  def sendMove(self, line, column):
    self.state.sendMove(self, line, column)

  def showLatency(self):
    self.state.showLatency(self)

  def endGame(self):
    self.state.endGame(self)

  def logout(self):
    self.state.logout(self)

def main():
  client = Client()
  command = input("JogoDaVelha> ").split()

  while command[0] != "bye":
    if command[0] == "new":
      if (len(command) < 3):
        print("Uso: new <username> <password>")
      else:
        client.createNewUser(command[1], command[2])

    elif command[0] == "pass":
      if (len(command) < 3):
        print("Uso: pass <old_password> <new_password>")
      else:
        client.changeUserPassword(command[1], command[2])

    elif command[0] == "in":
      if (len(command) < 3):
        print("Uso: in <username> <password>")
      else:
        client.loginUser(command[1], command[2])

    elif command[0] == "halloffame":
      client.showHallOfFame()

    elif command[0] == "l":
      client.showOnlinePlayers()

    elif command[0] == "call":
      if (len(command) < 2):
        print("Uso: call <opponent>")
      else:
        client.invitePlayer(command[1])

    elif command[0] == "play":
      if (len(command) < 3):
        print("Uso: play <linha> <coluna>")
      else:
        client.sendMove(command[1], command[2])

    elif command[0] == "delay":
      client.showLatency()

    elif command[0] == "over":
      client.endGame()

    elif command[0] == "out":
      client.logout()

    command = input("JogoDaVelha> ").split()


main()