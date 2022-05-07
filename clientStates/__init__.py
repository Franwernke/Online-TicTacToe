class InitialState():
  def createNewUser(self, user, password):
    print("Usuário: ", user, "Senha: ", password)
  
  def loginUser(self, user, password):
    print("Usuário: ", user, "Senha: ", password)
    return LoggedIn()

  def changeUserPassword(self, oldPassword, newPassword):
    print("Você precisa logar antes de alterar a senha!!!")


class LoggedIn():
  def createNewUser(self, user, password):
    print("Usuário: ", user, "Senha: ", password)
  
  def loginUser(self, user, password):
    print("Saia primeiro antes de logar em outra conta!!!")
    return self

  def changeUserPassword(self, oldPassword, newPassword):
    print("Senha antiga: ", oldPassword, "Senha atual: ", newPassword)