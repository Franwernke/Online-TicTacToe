from exceptions.GenericException import GenericException

class UserAlreadyLoggedIn(GenericException):
  def __init__(self):
    super().__init__("Usuário já logado!")