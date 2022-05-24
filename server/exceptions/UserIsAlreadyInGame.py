from exceptions.GenericException import GenericException

class UserIsAlreadyInGame(GenericException):
  def __init__(self):
    super().__init__("O usuário já está em jogo!")