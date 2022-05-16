from exceptions.GenericException import GenericException

class UserAlreadyExists(GenericException):
  def __init__(self):
    super().__init__("Usuário já existente!")