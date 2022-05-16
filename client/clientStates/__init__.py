class InitialState():
  def createNewUser(self, client, user, password):
    client.sendMessage("new " + user + " " + password)
  
  def loginUser(self, client, user, password):
    response = client.sendMessage("in " + user + " " + password)

    if response == "OK":
      client.user = user
      client.changeState(LoggedIn())
    else:
      print(response)

  def changeUserPassword(self, client, oldPassword, newPassword):
    print("Você precisa logar antes de alterar a senha!!!")

  def showHallOfFame(self, client):
    print("Hall of Fame: Francisco 1 Vinicius 1 tbm pq é lindo")
  
  def showOnlinePlayers(self, client):
    print("Vinicius (Francisco ta casado :( )")

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


class LoggedIn():
  def createNewUser(self, client, user, password):
    print("Usuário: ", user, "Senha: ", password)
  
  def loginUser(self, client, user, password):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, client, oldPassword, newPassword):
    print("Senha antiga: ", oldPassword, "Senha atual: ", newPassword)
  
  def showHallOfFame(self, client):
    print("Hall of Fame: Francisco 1 Vinicius 1 tbm pq é lindo")
  
  def showOnlinePlayers(self, client):
    print("Vinicius (Francisco ta casado :( )")

  def invitePlayer(self, client, opponent):
    print("Achando oponente...")
    if (opponent == "myturn"):
      client.changeState(MyTurn())
    else:
      client.changeState(HisTurn())

  def sendMove(self, client, line, column):
    print("Você não está jogando!!!")

  def showLatency(self, client):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self, client):
    print("Você não está em nenhuma partida!!!")

  def logout(self, client):
    print("deslologando")
    client.changeState(InitialState())

class MyTurn():
  def createNewUser(self, client, user, password):
    print("Espere a partida acabar para realizar esta ação")
  
  def loginUser(self, client, user, password):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, client, oldPassword, newPassword):
    print("Senha antiga: ", oldPassword, "Senha atual: ", newPassword)
  
  def showHallOfFame(self, client):
    print("Hall of Fame: Francisco 1 Vinicius 1 tbm pq é lindo")
  
  def showOnlinePlayers(self, client):
    print("Vinicius (Francisco ta casado :( )")

  def invitePlayer(self, client, opponent):
    print("usuario {opponent} te passas a bufa, aceitas?")

  def sendMove(self, client, line, column):
    print("Você não está jogando!!!")

  def showLatency(self, client):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self, client):
    print("Você não está em nenhuma partida!!!")

  def logout(self, client):
    print("deslologando")
    client.changeState(InitialState())

class HisTurn():
  def createNewUser(self, *args):
    print("Espere a partida acabar para realizar esta ação")
  
  def loginUser(self, *args):
    print("Saia primeiro antes de logar em outra conta!!!")

  def changeUserPassword(self, client, oldPassword, newPassword):
    print("Senha antiga: ", oldPassword, "Senha atual: ", newPassword)
  
  def showHallOfFame(self, *args):
    print("Hall of Fame: Francisco 1 Vinicius 1 tbm pq é lindo")
  
  def showOnlinePlayers(self, *args):
    print("Vinicius (Francisco ta casado :( )")

  def invitePlayer(self, *args):
    print("usuario {opponent} te passas a bufa, aceitas?")

  def sendMove(self, *args):
    print("Você não está jogando!!!")

  def showLatency(self, *args):
    print("Você não está conectado a nenhum player!!!")

  def endGame(self, *args):
    print("Você não está em nenhuma partida!!!")

  def logout(self, client):
    print("deslologando")
    client.changeState(InitialState())