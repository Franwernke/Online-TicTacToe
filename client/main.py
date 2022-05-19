import sys
from serverTCP import ServerTCP
from clientTCP import ClientTCP
from clientUDP import ClientUDP

def main():
  if sys.argv[3] == "tcp":
    client = ClientTCP(sys.argv[1], sys.argv[2])
  else:
    client = ClientUDP(sys.argv[1], sys.argv[2])

  server = ServerTCP()
  server.acceptConnections()

  command = input("JogoDaVelha> ").split()
  while command[0] != "bye":
    if command[0] == "new":
      if (len(command) < 3):
        print("Uso: new <username> <password>")
      else:
        client.createNewUser(command[1], command[2])

    elif command[0] == "pass":
      if (len(command) < 3):
        print("Uso: pass <old_password> <new_password>")
      else:
        client.changeUserPassword(command[1], command[2])

    elif command[0] == "in":
      if (len(command) < 3):
        print("Uso: in <username> <password>")
      else:
        client.loginUser(command[1], command[2], str(server.getPort()))

    elif command[0] == "halloffame":
      client.showHallOfFame()

    elif command[0] == "l":
      client.showOnlinePlayers()

    elif command[0] == "call":
      if (len(command) < 2):
        print("Uso: call <opponent>")
      else:
        client.invitePlayer(command[1])

    elif command[0] == "play":
      if (len(command) < 3):
        print("Uso: play <linha> <coluna>")
      else:
        client.sendMove(command[1], command[2])

    elif command[0] == "delay":
      client.showLatency()

    elif command[0] == "over":
      client.endGame()

    elif command[0] == "out":
      client.logout()

    command = input("JogoDaVelha> ").split()


main()