from exceptions.GenericException import GenericException

class UserNotFoundException(GenericException):
  def __init__(self):
    super().__init__("O usuário não foi encontrado")