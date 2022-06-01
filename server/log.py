import os

BASEPATH = "/tmp/ep2/"
LOGPATH = "log/"
LOGFILENAME = "log.will"

class Log:
  def __init__(self):
    if not os.path.exists(BASEPATH + LOGPATH):
      os.makedirs(BASEPATH + LOGPATH)
    
    file = open(BASEPATH + LOGPATH + LOGFILENAME, "w")
    file.write("Servidor iniciado!\n")
    file.close()

  def writeLogFile(self, text):
    file = open(BASEPATH + LOGPATH + LOGFILENAME, "a")
    file.write(text + "\n")
    file.close()

  def newConnection(self, ip):
    self.writeLogFile("Nova conexão." + " IP: " + str(ip))

  def newLogin(self, userName, success, ip):
    if success:
      self.writeLogFile("Usuário " + userName + " conseguiu logar." + " IP: " + str(ip)) 
    else:
      self.writeLogFile("Um cliente não conseguiu logar na conta " + userName + " IP: " + str(ip))

  def disconnect(self, ip):
    self.writeLogFile("Desconexão." + " IP: " + str(ip))

  def startgame(self, firstUser, secondUser, firstIp, secondIp):
    self.writeLogFile( 
      "Usuários " + firstUser + " e " + secondUser + 
      "com IPs: " + str(firstIp) + " e " +  str(secondIp) 
      + " inciam um novo jogo.")

  def finishGame(self, firstUser, secondUser, firstIp, secondIp, winner):
    self.writeLogFile( 
      "Usuários " + firstUser + " e " + secondUser + 
      "com IPs: " + str(firstIp) + " e " +  str(secondIp) 
      + " encerra o jogo. O ganhador foi: "+ winner)

  def unexpectedDisconnect(self, ip):
    self.writeLogFile("Desconexão inexperada." + " IP: " + str(ip))

  def finishServer(self):
    self.writeLogFile("Encerramento do servidor")