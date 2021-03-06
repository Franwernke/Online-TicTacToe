import os
from socket import *
from User import User
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.UserAlreadyExists import UserAlreadyExists
from exceptions.UserAlreadyLoggedIn import UserAlreadyLoggedIn
from exceptions.UserIsNotAvailable import UserIsNotAvailable
from UserSession import UserSession

BASEPATH = "/tmp/ep2/"
USERPATH = "users/"

class Repository:
  def __init__(self):
    if not os.path.exists(BASEPATH + "users"):
      os.makedirs(BASEPATH + "users") 

    if not os.path.exists(BASEPATH + "scores"):
      os.makedirs(BASEPATH + "scores")

    if not os.path.exists(BASEPATH + "online"):
      os.makedirs(BASEPATH + "online")

    for user in os.listdir(BASEPATH + "online"):
      os.remove(BASEPATH + "online/" + user)

  def createNewUser(self, user, password):
    if not os.path.exists(BASEPATH + USERPATH + user):
      file = open(BASEPATH + USERPATH + user, "w")
      file.write(password)
    else:
      raise UserAlreadyExists
  
  def createOnlinePlayer(self, user, p2paddress, port):
    if not os.path.exists(BASEPATH + "online/" + user):
      file = open(BASEPATH + "online/" + user, "w")
      file.write(user + " " + str(p2paddress[0]) + " " + str(p2paddress[1]) + " livre " 
                   + str(port))
    else:
      raise UserAlreadyLoggedIn

  def changeUserScore(self, user, score):
    file = open(BASEPATH + "scores/" + user, "w")
    file.write(str(score))
    file.close()

  def getUserScore(self, user):
    file = open(BASEPATH + "scores/" + user, "r")
    score = int(file.read())
    file.close()
    return score

  def getUser(self, user):
    if os.path.exists(BASEPATH + USERPATH + user):
      file = open(BASEPATH + USERPATH + user, "r")
      password = file.read()
      username = user
      return User(username, password)
    else:
      raise UserNotFoundException()

  def changePassword(self, user, newPassword):
    file = open(BASEPATH + USERPATH + user, "w")
    file.write(newPassword)

  def getScores(self):
    scores = dict()
    for user in os.listdir(BASEPATH + "scores"):
      file = open(BASEPATH + "scores/" + user)
      scores[user] = file.read()

    return scores

  def listOnlinePlayers(self):
    onlinePlayers = list()
    for user in os.listdir(BASEPATH + "online"):
      file = open(BASEPATH + "online/" + user)
      userData = file.read().split()
      onlinePlayers.append((user, userData[3]))

    return onlinePlayers

  def getOnlinePlayerByAddress(self, address):
    for user in os.listdir(BASEPATH + "online"):
      file = open(BASEPATH + "online/" + user)
      userData = file.read().split()

      if userData[1] == str(address[0]) and userData[4] == str(address[1]):
        return userData[0]

  def getOnlinePlayer(self, user):
    userSession = dict()
    if os.path.exists(BASEPATH + "online/" + user):
      file = open(BASEPATH + "online/" + user)
      userData = file.read().split()
      userSession = UserSession(user, userData[1], userData[2], userData[3])
      return userSession
    else:
      raise UserIsNotAvailable

  def removeOnlinePlayer(self, user):
    os.remove(BASEPATH + "online/" + user)

  def changeStatus(self, user, status):
    file = open(BASEPATH + "online/" + user, "r")
    data = file.read().split()
    file.close()
    data[3] = status

    file = open(BASEPATH + "online/" + user, "w")
    file.write(" ".join(data))
    file.close()
