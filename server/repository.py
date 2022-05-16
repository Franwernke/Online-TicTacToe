import os
from socket import *
from User import User
from exceptions.UserNotFoundException import UserNotFoundException

BASEPATH = "/tmp/ep2/"
USERPATH = "users/"

class Repository:
  def __init__(self):
    if not os.path.exists(BASEPATH + "users"):
      os.makedirs(BASEPATH + "users")

  def createNewUser(self, user, password):
    file = open(BASEPATH + USERPATH + user, "w")
    file.write(password)

  def getUser(self, user):
    if os.path.exists(BASEPATH + USERPATH + user):
      file = open(BASEPATH + USERPATH + user, "r")
      password = file.read()
      username = user
      return User(username, password)
    else:
      raise UserNotFoundException()