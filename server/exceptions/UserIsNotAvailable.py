from exceptions.GenericException import GenericException

class UserIsNotAvailable(GenericException):
  def __init__(self):
    super().__init__("Usuário não está disponível!")