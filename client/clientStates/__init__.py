from random import randint
from entities.ClientDomainI import ClientDomainI
from transportLayer.TCPLayer import TCPLayer
from entities.Game import Game

BASEPATH = '/tmp/ep2/client/'

class State:
  def __init__(self, client: ClientDomainI):
    self.client = client
    self.invitingUser: str = None
  
  def initialState(client):
    return InitialState(client)

class InitialState(State):
  def createNewUser(self, user, password):
    response = self.client.sendMessageToServer("new " + user + " " + password)
    if response == "OK":
      print("Usuário criado com sucesso!")
    else:
      print(response)
  
  def loginUser(self, user, password, port):
    response = self.client.sendMessageToServer("in " + user + " " + password + " " + port)
    if response == "OK":
      print("Login efetuado com sucesso!")
      self.client.user = user
      self.client.changeState(LoggedIn(self.client))
    else:
      print(response)

  def changeUserPassword(self, oldPassword, newPassword):
    print("Você precisa logar antes de alterar a senha!!!")

  def showHallOfFame(self):
    response = self.client.sendMessageToServer("halloffame")
    print(response)
  
  def showOnlinePlayers(self):
    response = self.client.sendMessageToServer("l")
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
    response = self.client.sendMessageToServer("pass " + self.client.user + " " + oldPassword + " " + newPassword)

    if response == "OK":
      print("Alteração de senha efetuada com sucesso!")
    else:
      print(response)
  
  def showHallOfFame(self):
    response = self.client.sendMessageToServer("halloffame")
    print(response)
  
  def showOnlinePlayers(self):
    response = self.client.sendMessageToServer("l")
    print(response)

  def invitePlayer(self, opponent):
    responseStr = self.client.sendMessageToServer("call " + self.client.user + " " + opponent)
    response = responseStr.split()

    if response[0] == "OK":
      self.client.createConnectionWithClient(response[1], response[2])
      responseStr = self.client.sendMessageToPeerToPeer("invite " + self.client.user)
      print("Esperando resposta do convite...")
      response = responseStr.split()

      if response[0] == "accept":
        myToken = response[2]
        opponentToken = "X" if myToken == "O" else "O"
        print("O oponente aceitou o convite!")
        response = self.client.sendMessageToServer("startgame " + self.client.user + " " + opponent)
        game = Game(opponentToken, opponent)
        self.client.changeState(HisTurn(self.client, game) if myToken == "O" else MyTurn(self.client, game))
      else:
        self.client.disconnectFromPlayer()
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
      self.client.sendMessageToPeerToPeerNoResp("P accept " + self.invitingUser + " " + opponentTurn)
      print("Você aceitou a partida!")
      game = Game(opponentTurn, self.invitingUser)
      self.invitingUser = None
      self.client.changeState(HisTurn(self.client, game) if opponentTurn == "X" else MyTurn(self.client, game))
    else:
      print("Ninguém te convidou! Você está bem?")

  def refuseGame(self):
    if self.invitingUser:
      self.client.sendMessageToPeerToPeerNoResp("P refuse " + self.invitingUser)
      self.invitingUser = None
      self.client.disconnectFromPlayer()
    else:
      print("Ninguém te convidou! Você está bem?")

  def sendMove(self, line, column):
    print("Você não está jogando!!!")

  def showLatency(self):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self):
    print("Você não está em nenhuma partida!!!")

  def logout(self):
    response = self.client.sendMessageToServer("out " + self.client.user)

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
    response = self.client.sendMessageToServer("halloffame")
    print(response)
  
  def showOnlinePlayers(self):
    response = self.client.sendMessageToServer("l")
    print(response)

  def invitePlayer(self, opponent):
    print("usuario {opponent} te passas a bufa, aceitas?")

  def sendMove(self, line, column):
    if not self.game.checkValidPlay(line, column):
      print("Insira uma jogada válida!")
      return
    self.game.markSpot(self.game.myToken, line, column)

    didWin = self.game.didWin(self.game.myToken)
    isDraw = self.game.isDraw()

    if didWin:
      self.game.printBoard()
    
      print("Você ganhou!!!")
      print("Você recebeu 3 pontos!")
   
      self.client.sendMessageToServer("won " + self.client.user + " " + self.game.opponentUser)
    elif isDraw:
      self.game.printBoard()
    
      print("Deu empate")
      print("Você recebeu 1 ponto")
    
      self.client.sendMessageToServer("draw " + self.client.user + " " + self.game.opponentUser)
    else:
      self.client.changeState(HisTurn(self.client, self.game))

    self.client.sendMessageToPeerToPeerNoResp("play " + str(line) + " " + str(column))

    if didWin or isDraw:
      self.client.changeState(LoggedIn(self.client))
      self.client.disconnectFromPlayer()

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
    response = self.client.sendMessageToServer("halloffame")
    print(response)
  
  def showOnlinePlayers(self):
    response = self.client.sendMessageToServer("l")
    print(response)

  def invitePlayer(self):
    print("usuario {opponent} te passas a bufa, aceitas?")

  def sendMove(self, line, column):
    print()
    self.game.markSpot(self.game.hisToken, line, column)
    
    if self.game.didWin(self.game.hisToken):
      self.game.printBoard()
      print("Você perdeu :(")
      print("Você recebeu 0 pontos")
      self.client.changeState(LoggedIn(self.client))
      self.client.disconnectFromPlayer()

    elif self.game.isDraw():
      self.game.printBoard()
      print("Deu empate")
      print("Você recebeu 1 ponto")
      self.client.changeState(LoggedIn(self.client))
      self.client.disconnectFromPlayer()
    
    else:
      self.client.changeState(MyTurn(self.client, self.game))
    
    print("JogoDaVelha> ", end="")

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