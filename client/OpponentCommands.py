from InputController import InputController

class OpponentCommands:
  def __init__(self, client) -> None:
    self.router = InputController(client)

  def handle(self, message):
    self.router.route(message)
