import os
from socket import *
from User import User
from exceptions.UserNotFoundException import UserNotFoundException
from exceptions.UserAlreadyExists import UserAlreadyExists

BASEPATH = "/tmp/ep2/"
USERPATH = "users/"

class Repository:
  def __init__(self):
    if not os.path.exists(BASEPATH + "users"):
      os.makedirs(BASEPATH + "users")

    if not os.path.exists(BASEPATH + "scores"):
      os.makedirs(BASEPATH + "scores")

  def createNewUser(self, user, password):
    if not os.path.exists(BASEPATH + USERPATH + user):
      file = open(BASEPATH + USERPATH + user, "w")
      file.write(password)
    else:
      raise UserAlreadyExists

  def changeUserScore(self, user, score):
    file = open(BASEPATH + "scores/" + user, "w")
    file.write(str(score))

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