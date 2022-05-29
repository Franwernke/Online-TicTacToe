from random import Random, randint, random
import re
from TCPLayer import TCPLayer
from Game import Game

BASEPATH = '/tmp/ep2/client/'

class State:
  def __init__(self, client):
    self.client = client
    self.invitingUser: str = None
  
  def initialState(client):
    return InitialState(client)

class InitialState(State):
  def createNewUser(self, user, password):
    response = self.client.sendMessage("new " + user + " " + password)
    if response == "OK":
      print("Usuário criado com sucesso!")
    else:
      print(response)
  
  def loginUser(self, user, password, port):
    response = self.client.sendMessage("in " + user + " " + password + " " + port)
    if response == "OK":
      print("Login efetuado com sucesso!")
      self.client.user = user
      self.client.changeState(LoggedIn(self.client))
    else:
      print(response)

  def changeUserPassword(self, oldPassword, newPassword):
    print("Você precisa logar antes de alterar a senha!!!")

  def showHallOfFame(self):
    response = self.client.sendMessage("halloffame")
    print(response)
  
  def showOnlinePlayers(self):
    response = self.client.sendMessage("l")
    print(response)

  def invitePlayer(self, opponent):
    print("Você precisa estar logado para jogar!!!")

  def sendMove(self, line, column):
    print("Você não está jogando!!!")

  def showLatency(self):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self):
    print("Você não está em nenhuma partida!!!")

  def logout(self):
    print("Você precisa estar logado!!!")

  def acceptGame(self, user):
    print("Você precisa estar logado!!!")

  def refuseGame(self, user):
    print("Você precisa estar logado!!!")



class LoggedIn(State):
  def createNewUser(self, user, password):
    print("Saia antes de criar um novo usuário!")
  
  def loginUser(self, user, password, port):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, oldPassword, newPassword):
    response = self.client.sendMessage("pass " + self.client.user + " " + oldPassword + " " + newPassword)

    if response == "OK":
      print("Alteração de senha efetuada com sucesso!")
    else:
      print(response)
  
  def showHallOfFame(self):
    response = self.client.sendMessage("halloffame")
    print(response)
  
  def showOnlinePlayers(self):
    response = self.client.sendMessage("l")
    print(response)

  def invitePlayer(self, opponent):
    responseStr = self.client.sendMessage("call " + self.client.user + " " + opponent)
    response = responseStr.split()

    if response[0] == "OK":
      self.client.opponentConnection = TCPLayer(response[1], response[2])
      self.client.opponentConnection.sendMessage("invite " + self.client.user)
      print("Esperando resposta do convite...")
      answer = self.client.opponentConnection.recvMessage().split()
      
      if answer[0] == "accept":
        myTurn = answer[2]
        print("O oponente aceitou o convite!")
        response = self.client.sendMessage("startgame " + self.client.user + " " + opponent)
        game = Game(myTurn)
        self.client.changeState(HisTurn(self.client, game) if myTurn == "O" else MyTurn(self.client, game))
      else:
        print("O oponente não aceitou o convite.")
      
    else:
      print(responseStr)

  def receiveInvite(self, invitingUser):
    print("Você recebeu um convite de " + invitingUser + ", deseja jogar?")
    print("Digite \"accept\" para aceitar e \"refuse\" para recusar")
    self.invitingUser = invitingUser
  
  def decideTurn(self):
    coin = randint(0, 1)
    return "O" if coin == 0 else "X"

  def acceptGame(self):
    if self.invitingUser:
      opponentTurn = self.decideTurn()
      self.client.peerToPeerServer.sendMessage("accept " + self.invitingUser + " " + opponentTurn)
      print("Você aceitou a partida!")
      self.invitingUser = None
      game = Game(opponentTurn)
      self.client.changeState(HisTurn(self.client, game) if opponentTurn == "X" else MyTurn(self.client, game))
      self.client.opponentConnection = self.client.peerToPeerServer
    else:
      print("Ninguém te convidou! Você está bem?")

  def refuseGame(self):
    if self.invitingUser:
      self.client.peerToPeerServer.sendMessage("refuse " + self.invitingUser)
      self.invitingUser = None
    else:
      print("Ninguém te convidou! Você está bem?")

  def sendMove(self, line, column):
    print("Você não está jogando!!!")

  def showLatency(self):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self):
    print("Você não está em nenhuma partida!!!")

  def logout(self):
    response = self.client.sendMessage("out " + self.client.user)

    if response == "OK":
      print("deslogado!")
      self.client.user = None
      self.client.changeState(InitialState(self.client))
    else:
      print(response)

class MyTurn(State):
  def __init__(self, client, game: Game):
    super().__init__(client)
    self.game = game
    self.game.printBoard()
    print("Seu turno! Digite play <linha> <coluna> para jogar")
  
  def createNewUser(self, user, password):
    print("Espere a partida acabar para realizar esta ação")
  
  def loginUser(self, user, password, port):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, oldPassword, newPassword):
    print("Senha antiga: ", oldPassword, "Senha atual: ", newPassword)
  
  def showHallOfFame(self):
    response = self.client.sendMessage("halloffame")
    print(response)
  
  def showOnlinePlayers(self):
    response = self.client.sendMessage("l")
    print(response)

  def invitePlayer(self, opponent):
    print("usuario {opponent} te passas a bufa, aceitas?")

  def sendMove(self, line, column):
    if not self.game.checkValidPlay(line, column):
      print("Insira uma jogada válida!")
      return
    self.game.markSpot(self.game.myToken, line, column)
    self.client.opponentConnection.sendMessage("play " + str(line) + " " + str(column))
    self.client.changeState(HisTurn(self.client, self.game))

  def showLatency(self):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self):
    print("Você não está em nenhuma partida!!!")

  def logout(self):
    print("Saia do jogo antes de deslogar!!!")

  def acceptGame(self, user):
    print("Saia do jogo atual antes de aceitar outro!!!")

  def refuseGame(self, user):
    print("Você precisa sair do jogo antes!!!")

class HisTurn(State):
  def __init__(self, client, game: Game):
    super().__init__(client)
    self.game = game
    self.game.printBoard()
    print("Turno dele! Espere a jogada do adversário")
  
  def createNewUser(self):
    print("Espere a partida acabar para realizar esta ação")
  
  def loginUser(self):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, oldPassword, newPassword):
    print("Senha antiga: ", oldPassword, "Senha atual: ", newPassword)
  
  def showHallOfFame(self):
    response = self.client.sendMessage("halloffame")
    print(response)
  
  def showOnlinePlayers(self):
    response = self.client.sendMessage("l")
    print(response)

  def invitePlayer(self):
    print("usuario {opponent} te passas a bufa, aceitas?")

  def sendMove(self, line, column):
    self.game.markSpot(self.game.hisToken, line, column)
    self.client.changeState(MyTurn(self.client, self.game))

  def showLatency(self):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self):
    print("Você não está em nenhuma partida!!!")

  def logout(self):
    print("Saia do jogo antes de deslogar!!!")

  def acceptGame(self, user):
    print("Saia do jogo atual antes de aceitar outro!!!")

  def refuseGame(self, user):
    print("Você precisa sair do jogo antes!!!")