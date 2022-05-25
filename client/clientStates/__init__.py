from TCPController import TCPController
import os

BASEPATH = '/tmp/ep2/client/'

class InitialState():
  def createNewUser(self, client, user, password):
    response = client.sendMessage("new " + user + " " + password)
    
    if response == "OK":
      print("Usuário criado com sucesso!")
    else:
      print(response)
  
  def loginUser(self, client, user, password, port):
    response = client.sendMessage("in " + user + " " + password + " " + port)

    if response == "OK":
      print("Login efetuado com sucesso!")
      client.user = user
      client.changeState(LoggedIn())
    else:
      print(response)

  def changeUserPassword(self, client, oldPassword, newPassword):
    print("Você precisa logar antes de alterar a senha!!!")

  def showHallOfFame(self, client):
    response = client.sendMessage("halloffame")
    print(response)
  
  def showOnlinePlayers(self, client):
    response = client.sendMessage("l")
    print(response)

  def invitePlayer(self, client, opponent):
    print("Você precisa estar logado para jogar!!!")

  def sendMove(self, client, line, column):
    print("Você não está jogando!!!")

  def showLatency(self, client):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self, client):
    print("Você não está em nenhuma partida!!!")

  def logout(self, client):
    print("Você precisa estar logado!!!")

  def acceptGame(self, user):
    print("Você precisa estar logado!!!")

  def refuseGame(self, user):
    print("Você precisa estar logado!!!")



class LoggedIn():
  def createNewUser(self, client, user, password):
    print("Saia antes de criar um novo usuário!")
  
  def loginUser(self, client, user, password, port):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, client, oldPassword, newPassword):
    response = client.sendMessage("pass " + client.user + " " + oldPassword + " " + newPassword)
  
    if response == "OK":
      print("Alteração de senha efetuada com sucesso!")
    else:
      print(response)
  
  def showHallOfFame(self, client):
    response = client.sendMessage("halloffame")
    print(response)
  
  def showOnlinePlayers(self, client):
    response = client.sendMessage("l")
    print(response)

  def invitePlayer(self, client, opponent):
    responseStr = client.sendMessage("call " + client.user + " " + opponent)
    response = responseStr.split()

    if response[0] == "OK":
      client.opponentConnection = TCPController(response[1], response[2])
      client.opponentConnection.sendMessage("invite " + client.user)
      answer = client.opponentConnection.recvMessage()
      print(answer)
    else:
      print(responseStr)

  def acceptGame(self, user):
    invitationsPath = BASEPATH + 'FIFOs/invitations/'
    if os.path.exists(invitationsPath + user):
      invitationFifo = open(invitationsPath + user, "w")
      invitationFifo.write("accept")
      invitationFifo.close()
    else:
      print("Este usuário não te convidou!")
      

  def refuseGame(self, user):
    invitationsPath = BASEPATH + 'FIFOs/invitations/'
    if os.path.exists(invitationsPath + user):
      invitationFifo = open(invitationsPath + user, "w")
      invitationFifo.write("refuse")
      invitationFifo.close()
    else:  
      print("Este usuário não te convidou!")
    

  def sendMove(self, client, line, column):
    print("Você não está jogando!!!")

  def showLatency(self, client):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self, client):
    print("Você não está em nenhuma partida!!!")

  def logout(self, client):
    response = client.sendMessage("out " + client.user)

    if response == "OK":
      print("deslogado!")
      client.user = None
      client.changeState(InitialState())
    else:
      print(response)

class MyTurn():
  def createNewUser(self, client, user, password):
    print("Espere a partida acabar para realizar esta ação")
  
  def loginUser(self, client, user, password, port):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, client, oldPassword, newPassword):
    print("Senha antiga: ", oldPassword, "Senha atual: ", newPassword)
  
  def showHallOfFame(self, client):
    response = client.sendMessage("halloffame")
    print(response)
  
  def showOnlinePlayers(self, client):
    response = client.sendMessage("l")
    print(response)

  def invitePlayer(self, client, opponent):
    print("usuario {opponent} te passas a bufa, aceitas?")

  def sendMove(self, client, line, column):
    print("Você não está jogando!!!")

  def showLatency(self, client):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self, client):
    print("Você não está em nenhuma partida!!!")

  def logout(self, client):
    print("Saia do jogo antes de deslogar!!!")

  def acceptGame(self, user):
    print("Saia do jogo atual antes de aceitar outro!!!")

  def refuseGame(self, user):
    print("Você precisa sair do jogo antes!!!")

class HisTurn():
  def createNewUser(self, *args):
    print("Espere a partida acabar para realizar esta ação")
  
  def loginUser(self, *args):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, client, oldPassword, newPassword):
    print("Senha antiga: ", oldPassword, "Senha atual: ", newPassword)
  
  def showHallOfFame(self, client):
    response = client.sendMessage("halloffame")
    print(response)
  
  def showOnlinePlayers(self, client):
    response = client.sendMessage("l")
    print(response)

  def invitePlayer(self, *args):
    print("usuario {opponent} te passas a bufa, aceitas?")

  def sendMove(self, *args):
    print("Você não está jogando!!!")

  def showLatency(self, *args):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self, *args):
    print("Você não está em nenhuma partida!!!")

  def logout(self, client):
    print("Saia do jogo antes de deslogar!!!")

  def acceptGame(self, user):
    print("Saia do jogo atual antes de aceitar outro!!!")

  def refuseGame(self, user):
    print("Você precisa sair do jogo antes!!!")