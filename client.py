#!/bin/python3

from clientStates import *

class Client:
  def __init__(self) -> None:
    self.state = InitialState()
    pass

  def createNewUser(self, user, password):
    self.state.createNewUser(user, password)

  def changeUserPassword(self, oldPassword, newPassword):
    self.state.changeUserPassword(oldPassword, newPassword)
  
  def loginUser(self, user, password):
    self.state = self.state.loginUser(user, password)

def main():
  client = Client()
  command = input("JogoDaVelha> ").split()

  while command[0] != "bye":
    if command[0] == "new":
      client.createNewUser(command[1], command[2])
    elif command[0] == "pass":
      client.changeUserPassword(command[1], command[2])
    elif command[0] == "in":
      client.loginUser(command[1], command[2])
    elif command[0] == "halloffame":
      client.showHallOfFame()
    elif command[0] == "l":
      client.showOnlinePlayers()
    elif command[0] == "call":
      client.invitePlayer(command[1])
    elif command[0] == "play":
      client.sendMove()
    elif command[0] == "delay":
      client.showLatency()
    elif command[0] == "over":
      client.endGame()
    elif command[0] == "out":
      client.logout()

    command = input("JogoDaVelha> ").split()


main()