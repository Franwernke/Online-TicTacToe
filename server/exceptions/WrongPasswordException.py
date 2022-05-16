from exceptions.GenericException import GenericException

class WrongPasswordException(GenericException):
  def __init__(self):
    super().__init__("Senha incorreta!")