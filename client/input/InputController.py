from Router import Router

class KeyboardCommands():
  validCommands = [
    "bye",
    "new",
    "pass",
    "in",
    "halloffame",
    "l",
    "call",
    "play",
    "delay",
    "over",
    "out",
    "accept",
    "refuse"
  ]
  bye = "bye"
  new = "new"
  Pass = "pass"
  In = "in"
  hallofame = "halloffame"
  l = "l"
  call = "call"
  play = "play"
  delay = "delay"
  over = "over"
  out = "out"
  accept = "accept"
  refuse = "refuse"

class InputController:
  def __init__(self, router: Router) -> None:
    self.router = router

  def listenToKeyboard(self):
    commandStr = input("JogoDaVelha> ")
    command = commandStr.split()
    while command[0] != KeyboardCommands.bye:
      if command[0] == KeyboardCommands.new:
        if (len(command) < 3):
          print("Uso: new <username> <password>")
        else:
          self.router.route(commandStr)

      elif command[0] == KeyboardCommands.Pass:
        if (len(command) < 3):
          print("Uso: pass <old_password> <new_password>")
        else:
          self.router.route(commandStr)

      elif command[0] == KeyboardCommands.In:
        if (len(command) < 3):
          print("Uso: in <username> <password>")
        else:
          self.router.route(commandStr)

      elif command[0] == KeyboardCommands.hallofame:
        self.router.route(commandStr)

      elif command[0] == KeyboardCommands.l:
         self.router.route(commandStr)

      elif command[0] == KeyboardCommands.call:
        if (len(command) < 2):
          print("Uso: call <opponent>")
        else:
          self.router.route(commandStr)

      elif command[0] == KeyboardCommands.play:
        if len(command) < 3:
          print("Uso: play <linha> <coluna>")
        else:
          self.router.route(commandStr)

      elif command[0] == KeyboardCommands.delay:
        self.router.route(commandStr)

      elif command[0] == KeyboardCommands.over:
        self.router.route(commandStr)

      elif command[0] == KeyboardCommands.out:
        self.router.route(commandStr)

      elif command[0] == KeyboardCommands.accept:
        self.router.route(commandStr)
        
      elif command[0] == KeyboardCommands.refuse:
        self.router.route(commandStr)

      else:
        print("Insira um comando válido!")

      commandStr = input("JogoDaVelha> ")
      command = commandStr.split()

    self.router.route(KeyboardCommands.bye)
