class UserSession:
  def __init__(self, username, ip, port, availability) -> None:
    self.username = username
    self.ip = ip
    self.port = port
    self.availability = availability